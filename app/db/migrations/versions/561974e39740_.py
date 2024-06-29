"""empty message

Revision ID: 561974e39740
Revises: b4b1db14b59e
Create Date: 2024-06-29 16:31:20.670105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '561974e39740'
down_revision: Union[str, None] = 'b4b1db14b59e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'bio',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Users', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Users', 'bio',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
