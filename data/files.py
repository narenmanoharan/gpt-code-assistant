
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from data.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUIDType(binary=False), ForeignKey("projects.id"))
    path = Column(String, unique=True)
    checksum = Column(String)
    index_id = Column(UUIDType(binary=False), ForeignKey("indexes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    file_sections = relationship("FileSection", cascade="all,delete-orphan")
