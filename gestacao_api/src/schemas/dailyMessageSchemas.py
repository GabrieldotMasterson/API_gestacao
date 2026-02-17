from pydantic import BaseModel
from src.models.dailyMessageModel import MessageCategory, MessageType


class DailyMessageSchema(BaseModel):
    message: str
    emoji: str
    category: MessageCategory
    type: MessageType
    only_premium: bool
    week_min: int
    week_max: int
    trimester: int


class DailyMessageSchemaPublic(BaseModel):
    id: int


class DailyMessageUpdate(BaseModel):
    message: str | None = None
    emoji: str | None = None
    category: str | None = None
    type: MessageType | None = None
