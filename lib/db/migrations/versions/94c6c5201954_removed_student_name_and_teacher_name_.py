"""removed student name and teacher name to Report_card

Revision ID: 94c6c5201954
Revises: aa70e45ab8a4
Create Date: 2023-07-17 17:08:11.222822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c6c5201954'
down_revision = 'aa70e45ab8a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('report cards', 'student_name')
    op.drop_column('report cards', 'teacher_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report cards', sa.Column('teacher_name', sa.VARCHAR(), nullable=True))
    op.add_column('report cards', sa.Column('student_name', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###