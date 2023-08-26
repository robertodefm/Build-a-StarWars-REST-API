"""empty message

Revision ID: 1406d00d507a
Revises: 3f42844388f4
Create Date: 2023-08-25 22:30:44.615928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1406d00d507a'
down_revision = '3f42844388f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'people', ['favorite_people_id'], ['id'])
        batch_op.create_foreign_key(None, 'planets', ['favorite_planet_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
