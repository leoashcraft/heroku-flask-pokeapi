"""empty message

Revision ID: 9dda69cabf8e
Revises: 4760f8da4786
Create Date: 2021-08-09 13:41:00.988709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dda69cabf8e'
down_revision = '4760f8da4786'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon')
    op.drop_table('person')
    op.drop_table('comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('pokemon_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], name='comment_pokemon_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['person.id'], name='comment_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comment_pkey')
    )
    op.create_table('person',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='person_pkey')
    )
    op.create_table('pokemon',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sprite', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('my_trait', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='pokemon_pkey')
    )
    # ### end Alembic commands ###
