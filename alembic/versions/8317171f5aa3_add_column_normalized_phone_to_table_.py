"""add column normalized_phone to table orders

Revision ID: 8317171f5aa3
Revises: 
Create Date: 2017-02-02 20:26:46.468660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8317171f5aa3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('normalized_phone', sa.String(length=10),
                                      nullable=True))


def downgrade():
    op.drop_column('orders', 'normalized_phone')
