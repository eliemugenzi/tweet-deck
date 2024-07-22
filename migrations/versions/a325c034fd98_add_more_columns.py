"""Add more columns...

Revision ID: a325c034fd98
Revises: aaf379de268f
Create Date: 2024-07-22 20:37:34.755327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a325c034fd98'
down_revision = 'aaf379de268f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lang', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('retweeted_status_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('in_reply_to_status_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('in_reply_to_user_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('in_reply_to_screen_name', sa.String(), nullable=True))
        batch_op.create_foreign_key(None, 'tweets', ['retweeted_status_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('in_reply_to_screen_name')
        batch_op.drop_column('in_reply_to_user_id')
        batch_op.drop_column('in_reply_to_status_id')
        batch_op.drop_column('retweeted_status_id')
        batch_op.drop_column('created_at')
        batch_op.drop_column('lang')

    # ### end Alembic commands ###