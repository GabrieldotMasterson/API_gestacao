from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.dailyMessageModel import DailyMessage
from src.schemas.dailyMessageSchemas import (
    DailyMessageSchema,
    DailyMessageSchemaPublic,
    DailyMessageUpdate
)

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(CurrentUser)]

router = APIRouter(prefix='/DailyMessage', tags=['DailyMessage'])


# ! Nao ir para o servidor final
@router.post('/', response_model=DailyMessageSchemaPublic)
async def create_message(
    dailyMessage: DailyMessageSchema,
    session: Session
): 

    db_message = DailyMessage(
        message = dailyMessage.message,
        emoji = dailyMessage.emoji,
        category = dailyMessage.category,
        emoji = dailyMessage.emoji,
    )