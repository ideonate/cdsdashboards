"""add dashboard presentation type

Revision ID: 260ac5c1a9e0
Revises: 2478e08b1ba2
Create Date: 2020-05-27 16:55:34.391858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '260ac5c1a9e0'
down_revision = '2478e08b1ba2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dashboards', sa.Column('presentation_type', sa.Unicode(255), default=''))


def downgrade():
    op.drop_column('dashboards', 'presentation_type')
