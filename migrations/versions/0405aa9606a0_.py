"""empty message

Revision ID: 0405aa9606a0
Revises: d9a5d504a5c5
Create Date: 2019-07-05 05:56:09.096578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0405aa9606a0'
down_revision = 'd9a5d504a5c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('line_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('campaign_name', sa.String(), nullable=True),
    sa.Column('line_item_name', sa.String(), nullable=True),
    sa.Column('booked_amount', sa.Float(), nullable=True),
    sa.Column('actual_amount', sa.Float(), nullable=True),
    sa.Column('adjustments', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('line_item')
    op.drop_table('invoice')
    # ### end Alembic commands ###
