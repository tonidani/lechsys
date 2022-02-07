"""empty message

Revision ID: 1401f97311dd
Revises: c2e08d069670
Create Date: 2021-09-02 21:59:10.689787

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1401f97311dd'
down_revision = 'c2e08d069670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('address', sa.String(length=128), nullable=True))
    op.drop_column('events', 'adress')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('adress', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('events', 'address')
    # ### end Alembic commands ###