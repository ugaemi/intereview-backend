"""Create user career table

Revision ID: d7ddf505c180
Revises: 967312b41f64
Create Date: 2022-11-12 20:31:47.901091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = "d7ddf505c180"
down_revision = "967312b41f64"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_career",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "company_id", sa.Integer, sa.ForeignKey("companies.id", ondelete="CASCADE")
        ),
        sa.Column("joined_date", sa.Date, default=func.now()),
        sa.Column("resignation_date", sa.Date, default=func.now()),
        sa.Column("created_datetime", sa.DateTime, default=func.now()),
        sa.Column(
            "updated_datetime",
            sa.DateTime,
            default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    op.drop_table("user_career")
