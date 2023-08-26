"""empty message

Revision ID: 3f42844388f4
Revises: 1336af6ab173
Create Date: 2023-08-25 22:28:04.637658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f42844388f4'
down_revision = '1336af6ab173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('favorite_planet_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_planet_id', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###