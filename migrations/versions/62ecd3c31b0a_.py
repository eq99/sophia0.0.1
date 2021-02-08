"""empty message

Revision ID: 62ecd3c31b0a
Revises: b5a136714f6f
Create Date: 2021-02-08 09:31:18.517924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ecd3c31b0a'
down_revision = 'b5a136714f6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('version', sa.Column('previous_version_id', sa.Integer(), nullable=True))
    op.drop_constraint('version_previous_version_fkey', 'version', type_='foreignkey')
    op.create_foreign_key(None, 'version', 'version', ['previous_version_id'], ['id'])
    op.drop_column('version', 'previous_version')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('version', sa.Column('previous_version', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'version', type_='foreignkey')
    op.create_foreign_key('version_previous_version_fkey', 'version', 'version', ['previous_version'], ['id'])
    op.drop_column('version', 'previous_version_id')
    # ### end Alembic commands ###