"""empty message

Revision ID: d9c6f3d51a4e
Revises: fa3f18bc8c98
Create Date: 2021-12-09 19:09:24.175258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9c6f3d51a4e'
down_revision = 'fa3f18bc8c98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contusion', sa.Column('body_part_id', sa.Integer(), nullable=True))
    op.add_column('contusion', sa.Column('tissue_id', sa.Integer(), nullable=True))
    op.add_column('contusion', sa.Column('trauma_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contusion', 'tissues', ['tissue_id'], ['id'])
    op.create_foreign_key(None, 'contusion', 'body_parts', ['body_part_id'], ['id'])
    op.create_foreign_key(None, 'contusion', 'traumas', ['trauma_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contusion', type_='foreignkey')
    op.drop_constraint(None, 'contusion', type_='foreignkey')
    op.drop_constraint(None, 'contusion', type_='foreignkey')
    op.drop_column('contusion', 'trauma_id')
    op.drop_column('contusion', 'tissue_id')
    op.drop_column('contusion', 'body_part_id')
    # ### end Alembic commands ###