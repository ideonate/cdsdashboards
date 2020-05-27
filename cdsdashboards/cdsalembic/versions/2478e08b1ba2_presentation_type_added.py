"""Presentation Type added

Revision ID: 2478e08b1ba2
Revises: 
Create Date: 2020-05-24 10:20:18.384756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2478e08b1ba2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dashboards', sa.Column('presentation_type', sa.Unicode(255), default=''))


def downgrade():
    op.drop_column('dashboards', 'presentation_type')
