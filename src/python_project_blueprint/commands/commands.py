from dataclasses import dataclass

class Command:
    """
    Base class for one-shot app commands.
    """

@dataclass(frozen=True)
class DisplayVersion(Command):
    uppercase: bool = False
