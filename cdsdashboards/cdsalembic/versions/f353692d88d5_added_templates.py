"""Added templates

Revision ID: f353692d88d5
Revises: 260ac5c1a9e0
Create Date: 2021-06-17 18:06:09.065414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f353692d88d5'
down_revision = '260ac5c1a9e0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('dashboards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('template_parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("dashboards_template_fk", 'dashboards', ['template_parent_id'], ['id'], ondelete='SET NULL')


def downgrade():
    with op.batch_alter_table('dashboards', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('template_parent_id')
