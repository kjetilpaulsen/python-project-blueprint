from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Session:
    session_id: str
    request_id: str
    cmd_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
