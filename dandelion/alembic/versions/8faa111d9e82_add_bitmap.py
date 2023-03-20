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

"""add_bitmap

Revision ID: 8faa111d9e82
Revises: a04def91cc98
Create Date: 2022-12-01 13:55:44.358393

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8faa111d9e82"
down_revision = "a8a42b36d109"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("map", sa.Column("bitmap_filename", sa.String(64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("map", "bitmap_filename")
    # ### end Alembic commands ###
