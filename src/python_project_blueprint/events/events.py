from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Event: 
    command_id: str

@dataclass(frozen=True)
class EvtLog(Event):
    message: str

@dataclass(frozen=True)
class EvtProgress(Event):
    current: int
    total: int
    message: str | None = None

@dataclass(frozen=True)
class EvtError(Event):
    message: str
    fatal: bool = True

@dataclass(frozen=True)
class EvtResult(Event):
    command_name: str
    payload: object

@dataclass(frozen=True)
class EvtRequest(Event):
    command_name: str
    payload: object
