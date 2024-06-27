"""endpoint_url_unique

Revision ID: 3792b8606230
Revises: 8e94d07ef559
Create Date: 2023-07-10 14:00:43.202137

"""
# import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3792b8606230"
down_revision = "8e94d07ef559"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("endpoint_url_unique", "endpoint", ["url"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("endpoint_url_unique", "endpoint", type_="unique")
    # ### end Alembic commands ###