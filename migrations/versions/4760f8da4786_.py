"""empty message

Revision ID: 4760f8da4786
Revises: 441c86e2e9e2
Create Date: 2021-08-06 11:21:50.299261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4760f8da4786'
down_revision = '441c86e2e9e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token_exp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'token_exp')
    # ### end Alembic commands ###
