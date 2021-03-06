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

"""Add RSI_CWM RSI_CLC RSI_SDS

Revision ID: a53f58b7c8b3
Revises: ffba191f33c8
Create Date: 2022-07-26 17:50:48.433222

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a53f58b7c8b3'
down_revision = 'ffba191f33c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rsi_clc',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.Column('msg_id', sa.String(length=255), nullable=False),
    sa.Column('sec_mark', sa.Integer(), nullable=False),
    sa.Column('veh_id', sa.String(length=255), nullable=False),
    sa.Column('ref_pos', sa.JSON(), nullable=False),
    sa.Column('drive_suggestion', sa.JSON(), nullable=False),
    sa.Column('info', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rsi_clc_id'), 'rsi_clc', ['id'], unique=False)
    op.create_table('rsi_cwm',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.Column('sensor_pos', sa.JSON(), nullable=True),
    sa.Column('event_type', sa.Integer(), nullable=False),
    sa.Column('collision_type', sa.Integer(), nullable=False),
    sa.Column('sec_mark', sa.Integer(), nullable=False),
    sa.Column('ego_id', sa.String(length=255), nullable=False),
    sa.Column('ego_pos', sa.JSON(), nullable=True),
    sa.Column('ego_heading', sa.Integer(), nullable=False),
    sa.Column('ego_radius', sa.Float(), nullable=False),
    sa.Column('ego_length', sa.Float(), nullable=False),
    sa.Column('ego_width', sa.Float(), nullable=False),
    sa.Column('ego_kinematics_info', sa.JSON(), nullable=True),
    sa.Column('other_id', sa.String(length=255), nullable=False),
    sa.Column('other_pos', sa.JSON(), nullable=True),
    sa.Column('other_heading', sa.Integer(), nullable=False),
    sa.Column('other_radius', sa.Float(), nullable=False),
    sa.Column('other_length', sa.Float(), nullable=False),
    sa.Column('other_width', sa.Float(), nullable=False),
    sa.Column('other_kinematics_info', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rsi_cwm_id'), 'rsi_cwm', ['id'], unique=False)
    op.create_table('rsi_sds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.Column('msg_id', sa.String(length=255), nullable=False),
    sa.Column('equipment_type', sa.Integer(), nullable=False),
    sa.Column('sensor_pos', sa.JSON(), nullable=True),
    sa.Column('sec_mark', sa.Integer(), nullable=False),
    sa.Column('ego_id', sa.String(length=255), nullable=False),
    sa.Column('ego_pos', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rsi_sds_id'), 'rsi_sds', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rsi_sds_id'), table_name='rsi_sds')
    op.drop_table('rsi_sds')
    op.drop_index(op.f('ix_rsi_cwm_id'), table_name='rsi_cwm')
    op.drop_table('rsi_cwm')
    op.drop_index(op.f('ix_rsi_clc_id'), table_name='rsi_clc')
    op.drop_table('rsi_clc')
    # ### end Alembic commands ###
