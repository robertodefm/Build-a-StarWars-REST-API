"""empty message

Revision ID: 1336af6ab173
Revises: 35bdac41e1aa
Create Date: 2023-08-25 22:27:13.774965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1336af6ab173'
down_revision = '35bdac41e1aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_people_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('favorite_planet_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_column('favorite_planet_id')
        batch_op.drop_column('favorite_people_id')

    # ### end Alembic commands ###
