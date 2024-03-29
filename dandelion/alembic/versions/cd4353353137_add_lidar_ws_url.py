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

"""add_lidar_ws_url

Revision ID: cd4353353137
Revises: cd1481c4a21d
Create Date: 2022-10-27 16:08:55.985589

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cd4353353137'
down_revision = 'cd1481c4a21d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lidar', sa.Column('ws_url', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lidar', 'ws_url')
    # ### end Alembic commands ###
