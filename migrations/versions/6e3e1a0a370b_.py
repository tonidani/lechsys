"""empty message

Revision ID: 6e3e1a0a370b
Revises: 5802a1c96ece
Create Date: 2021-12-06 20:45:42.609765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e3e1a0a370b'
down_revision = '5802a1c96ece'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kinase', sa.Column('state', sa.Text(), nullable=True))
    op.add_column('motoric', sa.Column('state', sa.Text(), nullable=True))
    op.add_column('rpe', sa.Column('state', sa.Text(), nullable=True))
    op.add_column('wellness', sa.Column('total_time', sa.Time(), nullable=True))
    op.add_column('wellness', sa.Column('state', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wellness', 'state')
    op.drop_column('wellness', 'total_time')
    op.drop_column('rpe', 'state')
    op.drop_column('motoric', 'state')
    op.drop_column('kinase', 'state')
    # ### end Alembic commands ###