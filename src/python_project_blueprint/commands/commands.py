from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Command:
    cmd_id: str # UUID

@dataclass(frozen=True)
class CmdDisplayVersion(Command): ...

