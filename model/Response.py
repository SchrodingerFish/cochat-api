from dataclasses import dataclass


@dataclass
class Response:
    status_code: int
    message: str
