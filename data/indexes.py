import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy_utils import UUIDType

from data.database import Base


class Index(Base):
    __tablename__ = "indexes"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUIDType(binary=False), ForeignKey("projects.id"))
    start_at = Column(DateTime, default=datetime.utcnow)
    end_at = Column(DateTime, nullable=True)
    indexed = Column(Integer, default=0, nullable=True)
    skipped = Column(Integer, default=0, nullable=True)
