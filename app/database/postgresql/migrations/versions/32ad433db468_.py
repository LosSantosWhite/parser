"""empty message

Revision ID: 32ad433db468
Revises: 
Create Date: 2023-07-03 00:04:00.903892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32ad433db468'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('fee', sa.BigInteger(), nullable=False),
    sa.Column('organizer', sa.String(), nullable=False),
    sa.Column('obj_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auction')
    # ### end Alembic commands ###
