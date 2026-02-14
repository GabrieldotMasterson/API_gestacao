from pydantic import BaseModel
from src.models.dailyMessageModel import MessageType


class DailyMessageSchema(BaseModel):
    message: str
    emoji: str
    category: str
    type: MessageType


class DailyMessageSchemaPublic(BaseModel):
    id: int


class DailyMessageUpdate(BaseModel):
    message: str | None = None
    emoji: str | None = None
    category: str | None = None
    type: MessageType | None = None


# todo:
