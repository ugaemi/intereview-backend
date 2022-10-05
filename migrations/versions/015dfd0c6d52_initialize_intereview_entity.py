"""Initialize intereview entity

Revision ID: 015dfd0c6d52
Revises:
Create Date: 2022-10-05 11:11:46.404178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = "015dfd0c6d52"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(12), unique=True, index=True),
        sa.Column("password", sa.String(20)),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("last_login", sa.DateTime, default=func.now()),
        sa.Column("joined_datetime", sa.DateTime, default=func.now()),
        sa.Column("withdrawal_datetime", sa.DateTime, nullable=True),
        sa.Column("created_datetime", sa.DateTime, default=func.now()),
        sa.Column(
            "updated_datetime",
            sa.DateTime,
            default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
