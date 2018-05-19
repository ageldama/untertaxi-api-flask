"""empty message

Revision ID: 11c80fabad17
Revises: 32214c9b9240
Create Date: 2018-05-19 18:16:32.038378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11c80fabad17'
down_revision = '32214c9b9240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ride_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('passenger_id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'BOOKED', 'ARRIVED', 'CANCELLED', name='ride_request_status'), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['member_addresses.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['members.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ride_requests')
    # ### end Alembic commands ###