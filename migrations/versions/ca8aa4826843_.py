"""empty message

Revision ID: ca8aa4826843
Revises: 
Create Date: 2020-05-05 16:31:08.246127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca8aa4826843'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('id_entrada', sa.Integer(), nullable=False),
    sa.Column('e_titulo', sa.String(length=100), nullable=False),
    sa.Column('e_cuerpo', sa.String(length=500), nullable=False),
    sa.Column('e_imagen', sa.String(length=250), nullable=True),
    sa.Column('e_fecha', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id_entrada')
    )
    op.create_table('tasks',
    sa.Column('ta_id', sa.Integer(), nullable=False),
    sa.Column('task01', sa.String(length=100), nullable=False),
    sa.Column('task02', sa.String(length=100), nullable=True),
    sa.Column('task03', sa.String(length=100), nullable=True),
    sa.Column('task04', sa.String(length=100), nullable=True),
    sa.Column('task05', sa.String(length=100), nullable=True),
    sa.Column('task06', sa.String(length=100), nullable=True),
    sa.Column('task07', sa.String(length=100), nullable=True),
    sa.Column('task08', sa.String(length=100), nullable=True),
    sa.Column('task09', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('ta_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('rut', sa.String(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('ciudad', sa.String(length=100), nullable=True),
    sa.Column('sexo', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('avatar', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('rut')
    )
    op.create_table('comentarios',
    sa.Column('id_comentario', sa.Integer(), nullable=False),
    sa.Column('c_cuerpo', sa.String(length=500), nullable=False),
    sa.Column('c_fecha', sa.String(length=200), nullable=False),
    sa.Column('id_blog', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id_blog'], ['blog.id_entrada'], ),
    sa.PrimaryKeyConstraint('id_comentario')
    )
    op.create_table('tramits',
    sa.Column('tr_id', sa.Integer(), nullable=False),
    sa.Column('tramit', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=10000), nullable=False),
    sa.Column('ta_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['ta_id'], ['tasks.ta_id'], ),
    sa.PrimaryKeyConstraint('tr_id'),
    sa.UniqueConstraint('tramit')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tramits')
    op.drop_table('comentarios')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('blog')
    # ### end Alembic commands ###
