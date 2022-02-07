"""empty message

Revision ID: bb27c0d93144
Revises: 1401f97311dd
Create Date: 2021-09-23 21:36:10.439631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb27c0d93144'
down_revision = '1401f97311dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('folder', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'folder')
    # ### end Alembic commands ###