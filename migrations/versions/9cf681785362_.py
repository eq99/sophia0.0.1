"""empty message

Revision ID: 9cf681785362
Revises: 16ab64525aa1
Create Date: 2021-02-04 19:32:27.787263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cf681785362'
down_revision = '16ab64525aa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created_time')
    # ### end Alembic commands ###
