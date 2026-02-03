from datetime import datetime
from enum import Enum

from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry
)

table_registry = registry()

class MessageType(str, Enum):
    floral = 'floral',
    oceano = 'oceano', 
    transformações = 'transformações',
    noite = 'noite',
    natureza = 'natureza'


# 'message':
#           'Você está fazendo um trabalho incrível. Cada dia é uma pequena vitória na sua jornada.',
#       'category': 'motivational',
#       'emoji': '🌸',    


@mapped_as_dataclass(table_registry)
class DailyMessage:
    __tablename__ = "dailyMessage"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    message: Mapped[str]
    category: Mapped[str]
    emoji: Mapped[str]
    type: Mapped[MessageType]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
