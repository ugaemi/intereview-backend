"""Create UserInfo table

Revision ID: a19170765811
Revises: 015dfd0c6d52
Create Date: 2022-10-05 11:18:14.778009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = "a19170765811"
down_revision = "015dfd0c6d52"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_infos",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("name", sa.String(20)),
        sa.Column("phone_country_code", sa.String(5)),
        sa.Column("phone_national_number", sa.String(12)),
        sa.Column("created_datetime", sa.DateTime, default=func.now()),
        sa.Column(
            "updated_datetime",
            sa.DateTime,
            default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    op.drop_table("user_infos")
