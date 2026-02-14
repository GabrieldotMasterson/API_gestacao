"""empty message

Revision ID: be25e2947b19
Revises: db199bc8ac30
Create Date: 2026-02-14 16:03:56.471736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be25e2947b19'
down_revision: Union[str, None] = 'db199bc8ac30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
