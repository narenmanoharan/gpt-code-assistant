
from datetime import datetime

from data.database import read_write_session
from data.indexes import Index
from data.projects import Project


def start_indexing(project: Project):
    """Start indexing the project."""
    with read_write_session() as session:
        index = Index(project_id=project.id)
        session.add(index)
        session.commit()
        return index.id

def complete_indexing(index_id: str, indexed: int, skipped: int):
    """Complete indexing the project."""
    with read_write_session() as session:
        index = session.query(Index).filter(Index.id == index_id).first()
        index.end_at = datetime.utcnow()
        index.indexed = indexed
        index.skipped = skipped
        session.commit()
