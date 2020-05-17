from sqlalchemy import Column, Boolean

from alvinchow_service.db.base import Base
from alvinchow_service.db.models.base import BaseModelMixin
from alvinchow_service.db.types import BigID, Text


"""
This is just a sample table, remove this (and alembic migration) in your real app!
"""
class User(BaseModelMixin, Base):
    __tablename__ = 'user'

    id = Column(BigID, primary_key=True)
    username = Column(Text)
    email = Column(Text)
    password = Column(Text)
    is_active = Column(Boolean)
