import pytest
from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from src.models.dailyMessageModel import DailyMessage
from src.models.userModel import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice',
            password='secret',
            email='teste@test',
            last_menstrual_period=time,
            pregnancy_date=time + relativedelta(months=9),
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert user.model_dump() == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'last_menstrual_period': time,
        'pregnancy_date': time + relativedelta(months=9),
    }


@pytest.mark.asyncio
async def test_create_daily_message(session, mock_db_time):

    daily_message = DailyMessage(
        message='Mensagem de teste',
        emoji='🔥',
        category='motivacional',
        type='padrão',
        only_premium=False,
        week_min=0,
        week_max=22,
        trimester=1
    )

    session.add(daily_message)
    await session.commit()

    daily_message = await session.scalar(select(DailyMessage))

    assert daily_message.model_dump() == {
        'id': 1,
        'message': 'Mensagem de teste',
        'emoji': '🔥',
        'category': 'motivacional',
        'type': 'padrão',
        'only_premium': False,
        'week_min': 0,
        'week_max': 22,
        'trimester': 1
    }
