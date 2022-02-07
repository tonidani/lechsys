"""empty message

Revision ID: b75e01c8c99c
Revises: 1bb12dafc394
Create Date: 2021-11-08 12:58:32.213809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b75e01c8c99c'
down_revision = '1bb12dafc394'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('hour', sa.Time(), nullable=True))
    op.add_column('events', sa.Column('details', sa.String(length=128), nullable=True))
    op.add_column('events', sa.Column('color', sa.String(length=128), nullable=True))
    op.drop_column('events', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('address', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('events', 'color')
    op.drop_column('events', 'details')
    op.drop_column('events', 'hour')
    # ### end Alembic commands ###
