"""delete_module_path

Revision ID: 8e94d07ef559
Revises: b1f155a1aeae
Create Date: 2023-06-09 17:05:47.937820

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "8e94d07ef559"
down_revision = "b1f155a1aeae"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("algo_name", "module_path")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("algo_name", sa.Column("module_path", mysql.VARCHAR(length=64), nullable=False))
    # ### end Alembic commands ###
