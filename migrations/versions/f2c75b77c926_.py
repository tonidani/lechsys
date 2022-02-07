"""empty message

Revision ID: f2c75b77c926
Revises: d4b13f914e54
Create Date: 2021-11-08 23:58:38.599645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c75b77c926'
down_revision = 'd4b13f914e54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('type', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'type')
    # ### end Alembic commands ###
