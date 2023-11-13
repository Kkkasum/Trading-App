"""Init Operation

Revision ID: d587c3fbea9f
Revises: e3021b0018b9
Create Date: 2023-11-10 00:09:26.110724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd587c3fbea9f'
down_revision: Union[str, None] = 'e3021b0018b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.Column('figi', sa.String(), nullable=True),
    sa.Column('instrument_type', sa.String(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation')
    # ### end Alembic commands ###