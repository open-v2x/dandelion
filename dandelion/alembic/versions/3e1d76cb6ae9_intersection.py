# Copyright 2022 99Cloud, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# flake8: noqa
# fmt: off

"""intersection

Revision ID: 3e1d76cb6ae9
Revises: a8a42b36d109
Create Date: 2022-11-25 14:57:22.864810

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3e1d76cb6ae9"
down_revision = "a8a42b36d109"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "intersection",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("create_time", sa.DateTime(), nullable=False),
        sa.Column("update_time", sa.DateTime(), nullable=False),
        sa.Column("area_code", sa.String(length=64), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("lng", sa.String(length=64), nullable=False),
        sa.Column("lat", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["area_code"], ["area.code"], name="intersection_fk_area"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("area_code", "name"),
    )
    op.create_index(op.f("ix_intersection_code"), "intersection", ["code"], unique=True)
    op.create_index(op.f("ix_intersection_id"), "intersection", ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_intersection_id"), table_name="intersection")
    op.drop_index(op.f("ix_intersection_code"), table_name="intersection")

    op.drop_table("intersection")
    # ### end Alembic commands ###
