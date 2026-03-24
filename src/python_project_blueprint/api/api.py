from __future__ import annotations

from contextlib import asynccontextmanager
import logging
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# FIX: change project name for imports
from python_project_blueprint.app import App
from python_project_blueprint.commands.buildcommands import build_commands
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.commands.frontendcommandinput import FrontendCommandInput 
from python_project_blueprint.events.events import (
    Event,
    EvtStarted,
    EvtFinished,
    EvtProgress,
    EvtLogMessage,
    EvtError,
    EvtResult,
    EvtRequestInput,

)
from python_project_blueprint.runtime.runtime import Runtime
from python_project_blueprint.utils.logging.setuplogging import ensure_setup_logging
from python_project_blueprint.utils.utils import resolve_version
from python_project_blueprint.runtime.logruntime import log_runtime

logger = logging.getLogger(__name__)

_RUNTIME: Runtime | None = None 



class APICommand(BaseModel):
    """
    Representation of a command requested through the HTTP API.

    This schema mirrors the frontend command structure used by the CLI
    layer. Each command contains a name identifying the command type
    and an optional dictionary of command-specific options.

    Attributes:
        name: Name of the command to execute.
        options: Command-specific options passed to the command handler.
    """
    name: Literal["version"]
    options: dict[str, Any] = Field(default_factory=dict)

class APIRunRequest(BaseModel):
    """
    Request body for the `/run` endpoint.

    The request contains optional runtime overrides together with the
    commands that should be executed by the application engine.

    Attributes:
        overrides: Runtime configuration overrides applied when executing
            the request.
        commands: List of commands requested by the client.
    """
    overrides: dict[str, Any] = Field(default_factory=dict)
    commands: list[APICommand]

class APIEvent(BaseModel):
    """
    Serialized representation of an application event returned by the API.

    Internal application `Event` objects are converted into this format
    before being returned to the client.

    Attributes:
        type: Event type identifier (for example `"log"`, `"progress"`,
            `"result"`, or `"error"`).
        data: Event-specific payload.
    """
    type: str
    data: dict[str, Any]

class APIRunResponse(BaseModel):
    """
    Response returned by the `/run` endpoint.

    Attributes:
        ok: Indicates whether the command execution completed successfully.
        events: List of serialized events produced by the application.
    """
    ok: bool
    events: list[APIEvent]

def _build_command_inputs(req: APIRunRequest) -> tuple[FrontendCommandInput,...]:
    """
    Convert API commands into frontend command inputs.

    The API layer uses its own request schemas. This function translates
    those schemas into `FrontendCommandInput` objects so the existing
    command-building pipeline can be reused.

    Args:
        req: Parsed API request containing command definitions.

    Returns:
        tuple[FrontendCommandInput, ...]: Normalized command inputs ready
        for conversion into executable `Command` objects.
    """
    return tuple(
        FrontendCommandInput(name=cmd.name, options=cmd.options)
        for cmd in req.commands
    )

def _event_to_api(evt: Event) -> APIEvent:
    """
    Convert an internal application event into an API event schema.

    The application engine produces internal `Event` objects. These are
    translated into `APIEvent` instances so they can be serialized and
    returned to HTTP clients.

    Args:
        evt: Internal event produced by the application runtime.

    Returns:
        APIEvent: Serialized representation of the event suitable for
        inclusion in an API response.
    """
    if isinstance(evt, EvtStarted):
        return APIEvent(type="evtstarted",
                        data={
                        "cmd_id": evt.cmd_id,
            },
        )
    if isinstance(evt, EvtFinished):
        return APIEvent(type="evtfinished",
                        data={
                        "cmd_id": evt.cmd_id,
                        "cmd_name": evt.cmd_name,
                        "ok": evt.ok,
                        "summary": evt.summary,
            },
        )
    if isinstance(evt, EvtProgress):
        return APIEvent(type="evtprogress",
                        data={
                        "cmd_id": evt.cmd_id,
                        "current": evt.current,
                        "total": evt.total,
                        "message": evt.message,
            },
        )
    if isinstance(evt, EvtLogMessage):
        return APIEvent(type="evtlogmessage", 
                        data={
                        "cmd_id": evt.cmd_id,
                        "level": evt.level,
                        "message": evt.message,
            },
        )
    if isinstance(evt, EvtError):
        return APIEvent(type="evterror",
                        data={
                        "cmd_id": evt.cmd_id,
                        "code": evt.code,
                        "message": evt.message,
                        "fatal": evt.fatal,
                        "details": evt.details,
            },
        )

    if isinstance(evt, EvtResult):
        return APIEvent(type="evtresult",
                        data={
                        "cmd_id": evt.cmd_id,
                        "result_type": evt.result_type,
                        "payload": evt.payload,
                        "is_final": evt.is_final,
            },
        )
    if isinstance(evt, EvtRequestInput):
        return APIEvent(type="evtrequestinput",
                        data={
                        "cmd_id": evt.cmd_id,
                        "request_id": evt.request_id,
                        "prompt": evt.prompt,
                        "input_kind": evt.input_kind,
                        "field_name": evt.field_name,
                        "required": evt.required,
                        "choices": evt.choices,
            },
        )

    return APIEvent(
        type="unknown",
        data={"event_class": type(evt).__name__},
    )

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Application lifecycle manager for the FastAPI server.

    This function initializes the application runtime when the API
    server starts. Runtime configuration and logging are set up once
    during startup and reused for all incoming requests.

    Args:
        _: The FastAPI application instance (unused).

    Yields:
        None: Control is yielded back to FastAPI while the application
        is running.
    """
    global _RUNTIME

    _RUNTIME = build_runtime()

    ensure_setup_logging(
        IDENTITY.logger_name,
        _RUNTIME.paths,
        _RUNTIME.log,
    )
    log_runtime(_RUNTIME)

    logger.info("API runtime initialized")
    yield

api = FastAPI(
    title=IDENTITY.app_name,
    version=resolve_version(),
    description="HTTP API frontend.",
    lifespan=lifespan,
    )

@api.get("/health")
def health() -> dict[str, str]:
    """
    Health check endpoint.

    This endpoint can be used by monitoring systems or container
    orchestrators to verify that the API server is running.

    Returns:
        dict[str, str]: Simple status indicator.
    """
    return {"status": "ok"}

@api.post("/run", response_model=APIRunResponse)
def run_commands(req: APIRunRequest) -> APIRunResponse:
    """
    Execute commands through the API.

    The request is translated into internal command objects and executed
    by the application engine. Events produced during execution are
    converted into API-compatible representations and returned in the
    response.

    Args:
        req: API request describing commands and optional runtime overrides.

    Returns:
        APIRunResponse: Structured response containing execution events.

    Raises:
        HTTPException: If runtime initialization failed, invalid commands
        were supplied, or an internal error occurred.
    """
    if _RUNTIME is None:
        raise HTTPException(status_code=500, detail="Runtime not initialized")

    try:
        frontendinputcommands = _build_command_inputs(req)
        # commands = build_commands(command_inputs)
        queue: list[Command] = [build_commands(cmd) for cmd in frontendinputcommands]

        app = App(_RUNTIME.meta, _RUNTIME.dev, _RUNTIME.db, _RUNTIME.paths)
        while queue:
            cmd, *queue = queue
            for evt in app.run(cmd):
                if isinstance(evt, EvtError) and evt.fatal:
                    logger.error("Fatal error in command %s; %s", cmd.cmd_id, evt.message)
                    break

                new_cmd = _event_to_api(evt)
                if isinstance(new_cmd, Command):
                    queue.append(new_cmd)


        # events = [_event_to_api(evt) for evt in app.run(commands)]

        return APIRunResponse(ok=True, events=events)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unhandled API error")
        raise HTTPException(status_code=500, detail="Internal server error") from exc

