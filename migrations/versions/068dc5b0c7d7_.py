"""empty message

Revision ID: 068dc5b0c7d7
Revises: 685cff1741b9
Create Date: 2020-02-16 12:42:44.957546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '068dc5b0c7d7'
down_revision = '685cff1741b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meal', 'title',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meal', 'title',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###