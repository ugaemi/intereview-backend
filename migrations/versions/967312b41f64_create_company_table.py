"""Create company table

Revision ID: 967312b41f64
Revises: a19170765811
Create Date: 2022-11-12 20:29:54.612603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = "967312b41f64"
down_revision = "a19170765811"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(50)),
        sa.Column("corporate_registration_number", sa.String(20), nullable=True),
        sa.Column("company_registration_number", sa.String(20), nullable=True),
        sa.Column("address", sa.String(100), nullable=True),
        sa.Column("address_detail", sa.String(100), nullable=True),
        sa.Column("zip_code", sa.String(10), nullable=True),
        sa.Column("homepage_url", sa.String(200), nullable=True),
        sa.Column("phone_country_code", sa.String(5), nullable=True),
        sa.Column("phone_national_number", sa.String(12), nullable=True),
        sa.Column("logo_url", sa.String(200), nullable=True),
        sa.Column("created_datetime", sa.DateTime, default=func.now()),
        sa.Column(
            "updated_datetime",
            sa.DateTime,
            default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    op.drop_table("companies")
