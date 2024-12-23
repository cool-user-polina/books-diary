"""added author to base

Revision ID: ba1f3a9009d9
Revises: 34992ce8ec07
Create Date: 2024-11-14 18:01:27.532132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba1f3a9009d9'
down_revision = '34992ce8ec07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('base', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('base', schema=None) as batch_op:
        batch_op.drop_column('author')

    # ### end Alembic commands ###
