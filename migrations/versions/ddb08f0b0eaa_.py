"""empty message

Revision ID: ddb08f0b0eaa
Revises: 
Create Date: 2020-04-29 15:45:06.631419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddb08f0b0eaa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('rut', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('ciudad', sa.String(length=100), nullable=True),
    sa.Column('sexo', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('rut')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###