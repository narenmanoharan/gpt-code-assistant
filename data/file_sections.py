
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy_utils import UUIDType

from data.database import Base


class FileSection(Base):
    __tablename__ = "file_sections"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUIDType(binary=False), ForeignKey("files.id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
