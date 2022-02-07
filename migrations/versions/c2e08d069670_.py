"""empty message

Revision ID: c2e08d069670
Revises: 91138acdbb62
Create Date: 2021-09-02 21:57:26.929761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2e08d069670'
down_revision = '91138acdbb62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('adress', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'adress')
    # ### end Alembic commands ###
