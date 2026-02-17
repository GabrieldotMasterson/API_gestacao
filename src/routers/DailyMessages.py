from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models.dailyMessageModel import DailyMessage
from src.schemas.dailyMessageSchemas import (
    DailyMessageSchema,
    DailyMessageSchemaPublic,
)

Session = Annotated[AsyncSession, Depends(get_session)]
router = APIRouter(prefix='/DailyMessage', tags=['DailyMessage'])


# ! Nao ir para o servidor final
@router.post('/', response_model=DailyMessageSchemaPublic)
async def create_daily_message(
    dailyMessage: DailyMessageSchema, session: Session
):

    db_message = DailyMessage(
        message=dailyMessage.message,
        emoji=dailyMessage.emoji,
        category=dailyMessage.category,
        type=dailyMessage.type,
        only_premium=dailyMessage.only_premium,
    )
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)

    return db_message


@router.get('/{message_id}', response_model=DailyMessageSchemaPublic)
async def get_daily_message(
    session: Session,
    message_id: int,
):

    query = select(DailyMessage).where(DailyMessage.id == message_id)

    result = await session.exec(query)
    dailyMessage = result.first()

    if not dailyMessage:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Daily message not found'
        )

    return dailyMessage
