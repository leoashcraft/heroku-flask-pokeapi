"""empty message

Revision ID: 60f14b0fc74d
Revises: f12472cff656
Create Date: 2021-08-09 13:55:11.622660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60f14b0fc74d'
down_revision = 'f12472cff656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('pokemon_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='comment_pkey')
    )
    # ### end Alembic commands ###
