import enum
from dataclasses import dataclass
from typing import Optional


class ValidCommands(enum.Enum):
    SET = "SET"
    GET = "GET"
    DELETE = "DELETE"
    EXISTS = "EXISTS"


@dataclass
class ParsedCommand:
    type: ValidCommands
    key: Optional[str] = None 
    value: Optional[str] = None