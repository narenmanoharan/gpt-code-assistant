
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from data.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    path = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    files = relationship("File", cascade="all,delete-orphan")
    indexes = relationship("Index", cascade="all,delete-orphan")
