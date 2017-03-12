"""empty message

Revision ID: b99429f20e58
Revises: 90c591ad3f51
Create Date: 2017-03-12 00:49:05.927893

"""

# revision identifiers, used by Alembic.
revision = 'b99429f20e58'
down_revision = '90c591ad3f51'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('department', sa.String(length=255), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=False),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_email'), 'employee', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employee_email'), table_name='employee')
    op.drop_table('employee')
    # ### end Alembic commands ###