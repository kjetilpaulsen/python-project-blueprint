from python_project_blueprint.commands.commands import CmdDisplayVersion
from python_project_blueprint.handlers.displayversionhandler import DisplayVersionHandler
from python_project_blueprint.runtime.runtime import MetaInfo
from python_project_blueprint.events.events import EvtResult


def test_display_version_handler_returns_evtresult():
    cmd = CmdDisplayVersion(
        uppercase=False,

    )
    meta = MetaInfo(
        app_name="python-project-blueprint",
        app_version="1.2.3",
        app_description="test app",
    )

    handler = DisplayVersionHandler(cmd, meta)

    events = list(handler.handle())

    assert len(events) == 1
    assert isinstance(events[0], EvtResult)
    assert events[0].command_name == "DisplayVersion"
    assert events[0].payload == {"version": "v1.2.3"}
