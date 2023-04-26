"""algo_platform

Revision ID: cb43f864daea
Revises: 26c910b0342f
Create Date: 2023-04-23 17:16:47.148649

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "cb43f864daea"
down_revision = "26c910b0342f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("algo_version", sa.Column("endpoint_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "algo_version_endpoint_fk", "algo_version", "endpoint", ["endpoint_id"], ["id"]
    )
    op.drop_column("algo_version", "version_path")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "algo_version", sa.Column("version_path", mysql.VARCHAR(length=64), nullable=True)
    )
    op.drop_constraint("algo_version_endpoint_fk", "algo_version", type_="foreignkey")
    op.drop_column("algo_version", "endpoint_id")
    # ### end Alembic commands ###
