from __future__ import annotations

from contextlib import asynccontextmanager
from importlib import metadata
import logging
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from python_project_blueprint.app import App
from python_project_blueprint.commands.buildcommands import build_commands
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.runtime.parsedinput import FrontendCommandInput, CliParsedInput, RuntimeOverrides
from python_project_blueprint.events.events import Event, EvtLog, EvtProgress, EvtError, EvtResult
from python_project_blueprint.runtime.runtime import Runtime
from python_project_blueprint.utils.logging.loggingsetup import ensure_logging_setup, logging_basic_setup, logging_setup
from python_project_blueprint.utils.logging.logruntime import log_runtime

logger = logging.getLogger(__name__)

_RUNTIME: Runtime | None = None 

def _resolve_version() -> str:
    try:
        return metadata.version(IDENTITY.dist_name)
    except metadata.PackageNotFoundError:
        return "Cannot resolve version"


class APICommand(BaseModel):
    name: Literal["version"]
    options: dict[str, Any] = Field(default_factory=dict)

class APIRunRequest(BaseModel):
    overrides: dict[str, Any] = Field(default_factory=dict)
    commands: list[APICommand]

class APIEvent(BaseModel):
    type: str
    data: dict[str, Any]

class APIRunResponse(BaseModel):
    ok: bool
    events: list[APIEvent]

def _build_command_inputs(req: APIRunRequest) -> tuple[FrontendCommandInput,...]:
    return tuple(
        FrontendCommandInput(name=cmd.name, options=cmd.options)
        for cmd in req.commands
    )

def _event_to_api(evt: Event) -> APIEvent:
    if isinstance(evt, EvtLog):
        return APIEvent(type="log", data={"message": evt.message})

    if isinstance(evt, EvtProgress):
        return APIEvent(
            type="progress",
            data={
                "current": evt.current,
                "total": evt.total,
                "message": evt.message,
            },
        )

    if isinstance(evt, EvtError):
        return APIEvent(
            type="error",
            data={
                "message": evt.message,
                "fatal": evt.fatal,
            },
        )

    if isinstance(evt, EvtResult):
        return APIEvent(
            type="result",
            data={
                "command_name": evt.command_name,
                "payload": evt.payload,
            },
        )

    return APIEvent(
        type="unknown",
        data={"event_class": type(evt).__name__},
    )

@asynccontextmanager
async def lifespan(_: FastAPI):
    global _RUNTIME

    _RUNTIME = build_runtime()

    ensure_logging_setup(
        IDENTITY.logger_name,
        _RUNTIME.paths,
        _RUNTIME.log,
    )
    log_runtime(_RUNTIME)

    logger.info("API runtime initialized")
    yield

api = FastAPI(
    title=IDENTITY.app_name,
    version=_resolve_version(),
    description="HTTP API frontend.",
    lifespan=lifespan,
    )

@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@api.post("/run", response_model=APIRunResponse)
def run_commands(req: APIRunRequest) -> APIRunResponse:
    if _RUNTIME is None:
        raise HTTPException(status_code=500, detail="Runtime not initialized")

    try:
        command_inputs = _build_command_inputs(req)
        commands = build_commands(command_inputs)

        app = App(_RUNTIME.meta, _RUNTIME.dev, _RUNTIME.db, _RUNTIME.paths)
        events = [_event_to_api(evt) for evt in app.run(commands)]

        return APIRunResponse(ok=True, events=events)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unhandled API error")
        raise HTTPException(status_code=500, detail="Internal server error") from exc

