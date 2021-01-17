from sqlalchemy import Column, Index, Boolean

from alvinchow_backend.db.base import Base
from alvinchow_backend.db.models.base import BaseModelMixin
from alvinchow_backend.db.types import BigIntegerID, Text, UTCDateTime


"""
This is just a sample table, remove this (and alembic migration) in your real app!
"""


class User(BaseModelMixin, Base):
    __tablename__ = 'user'

    id = Column(BigIntegerID, primary_key=True)
    email = Column(Text)
    email_verified_at = Column(UTCDateTime)

    password = Column(Text)
    password_updated_at = Column(UTCDateTime)

    is_active = Column(Boolean, default=True)
    last_login_time = Column(UTCDateTime)

    __table_args__ = (
        Index('ix_user_email_unique', email, unique=True, postgresql_where=(
            email_verified_at.isnot(None)
        )),
    )

    def __repr__(self):
        return f'<User(id={self.id}, email={self.email})>'
