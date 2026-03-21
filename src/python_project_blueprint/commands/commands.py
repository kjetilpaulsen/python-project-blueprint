from dataclasses import dataclass

class Command:
    """
    Base class for one-shot app commands.
    """

@dataclass(frozen=True)
class CmdDisplayVersion(Command):
    uppercase: bool = False

@dataclass(frozen=True)
class CmdNextProgress: ...

@dataclass(frozen=True)
class CmdExit: ...
