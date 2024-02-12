from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Request:
    version: Optional[int]
    model: str
    messages: List[Message]

    @classmethod
    def build_request(cls, model: str, message_data: List[dict]):
        messages = [Message(role=msg["role"], content=msg["content"]) for msg in message_data]
        return cls(model=model, messages=messages)
