"""empty message

Revision ID: bea4d6ad2c77
Revises: d6e5bb3ef620
Create Date: 2021-10-02 22:25:49.242624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bea4d6ad2c77'
down_revision = 'd6e5bb3ef620'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('language', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'language')
    # ### end Alembic commands ###
