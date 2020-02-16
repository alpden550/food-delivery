"""empty message

Revision ID: 685cff1741b9
Revises: f4377538b737
Create Date: 2020-02-16 12:36:38.547175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '685cff1741b9'
down_revision = 'f4377538b737'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meal', 'description',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=400),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meal', 'description',
               existing_type=sa.String(length=400),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    # ### end Alembic commands ###
