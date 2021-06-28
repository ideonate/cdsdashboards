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

naming_convention = {
    "fk":
    "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

def upgrade():
    with op.batch_alter_table('dashboards', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint("fk_dashboards_source_spawner_id_spawners", type_='foreignkey')
        batch_op.drop_column('source_spawner_id')
        batch_op.add_column(sa.Column('template_parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("dashboards_template_fk", 'dashboards', ['template_parent_id'], ['id'], ondelete='SET NULL')


def downgrade():
    with op.batch_alter_table('dashboards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source_spawner_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'spawners', ['source_spawner_id'], ['id'], ondelete='SET NULL')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('template_parent_id')
