from dataclasses import asdict

import pytest
from sqlalchemy import select
from src.models import Todo, User

from dateutil.relativedelta import relativedelta


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'last_menstrual_period' : time,
        'pregnancy_date': time + relativedelta(months=9),
        'todos': [],
        # 'updated_at': time,  # Exercício
    }


# @pytest.mark.asyncio
# async def test_create_todo(session, user: User):
#     todo = Todo(
#         title='Test Todo',
#         description='Test Desc',
#         state='draft',
#         user_id=user.id,
#     )

#     session.add(todo)
#     await session.commit()

#     todo = await session.scalar(select(Todo))

#     assert asdict(todo) == {
#         'description': 'Test Desc',
#         'id': 1,
#         'state': 'draft',
#         'title': 'Test Todo',
#         'user_id': 1,
#     }
