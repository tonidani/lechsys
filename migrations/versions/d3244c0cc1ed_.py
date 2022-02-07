"""empty message

Revision ID: d3244c0cc1ed
Revises: f2c75b77c926
Create Date: 2021-11-10 20:19:13.840928

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd3244c0cc1ed'
down_revision = 'f2c75b77c926'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('id', table_name='types')
    op.drop_table('types')
    op.add_column('events', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'event_types', ['type_id'], ['id'])
    op.drop_column('events', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('type', mysql.VARCHAR(length=128), nullable=True))
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'type_id')
    op.create_table('types',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('id', 'types', ['id'], unique=False)
    # ### end Alembic commands ###