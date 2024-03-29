"""rse_name_not_repeat

Revision ID: b1f155a1aeae
Revises: cb43f864daea
Create Date: 2023-05-05 10:31:53.774217

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "b1f155a1aeae"
down_revision = "cb43f864daea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_camera_name", table_name="camera")
    op.create_index(op.f("ix_camera_name"), "camera", ["name"], unique=True)
    op.drop_index("ix_lidar_name", table_name="lidar")
    op.create_index(op.f("ix_lidar_name"), "lidar", ["name"], unique=True)
    op.drop_index("ix_radar_name", table_name="radar")
    op.create_index(op.f("ix_radar_name"), "radar", ["name"], unique=True)
    op.drop_index("ix_rsu_rsu_name", table_name="rsu")
    op.create_index(op.f("ix_rsu_rsu_name"), "rsu", ["rsu_name"], unique=True)
    op.drop_index("ix_spat_name", table_name="spat")
    op.create_index(op.f("ix_spat_name"), "spat", ["name"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_spat_name"), table_name="spat")
    op.create_index("ix_spat_name", "spat", ["name"], unique=False)
    op.drop_index(op.f("ix_rsu_rsu_name"), table_name="rsu")
    op.create_index("ix_rsu_rsu_name", "rsu", ["rsu_name"], unique=False)
    op.drop_index(op.f("ix_radar_name"), table_name="radar")
    op.create_index("ix_radar_name", "radar", ["name"], unique=False)
    op.drop_index(op.f("ix_lidar_name"), table_name="lidar")
    op.create_index("ix_lidar_name", "lidar", ["name"], unique=False)
    op.drop_index(op.f("ix_camera_name"), table_name="camera")
    op.create_index("ix_camera_name", "camera", ["name"], unique=False)
    # ### end Alembic commands ###
