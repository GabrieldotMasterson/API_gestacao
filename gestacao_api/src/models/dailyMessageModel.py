from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class MessageType(str, Enum):
    floral = 'floral',
    ocean = 'oceano', 
    transformations = 'transformações',
    night = 'noite',
    nature = 'natureza'
    body = 'seu corpo'


# 'message':
#           'Você está fazendo um trabalho incrível. Cada dia é uma pequena vitória na sua jornada.',
#       'category': 'motivational',
#       'emoji': '🌸',    


class DailyMessage(SQLModel, table=True):
    __tablename__ = "daily_message_widgets"

    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    category: str
    emoji: str
    type: MessageType

    user_id: int = Field(foreign_key="users.id")