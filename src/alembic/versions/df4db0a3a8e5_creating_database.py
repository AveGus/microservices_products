"""creating database

Revision ID: df4db0a3a8e5
Revises: f99d8f06f041
Create Date: 2024-09-12 16:16:36.069481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'df4db0a3a8e5'
down_revision: Union[str, None] = 'f99d8f06f041'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    product_type = op.create_table('product_type',
                                   sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                                   sa.Column('name', sa.VARCHAR(length=255), nullable=False),
                                   sa.PrimaryKeyConstraint('id')
                                   )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
                    sa.Column('product_type_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.bulk_insert(product_type, [
        {
            "id": 1,
            "name": "juice"
        }
    ])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('product_type')
    # ### end Alembic commands ###
