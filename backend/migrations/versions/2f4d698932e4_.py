"""empty message

Revision ID: 2f4d698932e4
Revises: 
Create Date: 2022-12-15 12:01:43.088113

"""
from alembic import op
import sqlalchemy as sa

# REMEMBER TO GET UUID WORKING
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '2f4d698932e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email')
    )
    op.create_table('scores',
    sa.Column('user_email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('user_email', 'created_at')
    )
    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_scores_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_scores_score'), ['score'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_scores_score'))
        batch_op.drop_index(batch_op.f('ix_scores_created_at'))

    op.drop_table('scores')
    op.drop_table('users')
    # ### end Alembic commands ###