from typing import List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from data.chroma import get_file_section_collection
from data.database import read_only_session
from data.file_sections import FileSection
from data.files import File


class MatchResult(BaseModel):
    path: str
    similarity: float
    content: str

def match_file_sections(project_id: UUID, query_embedding) -> List[MatchResult]:
    results = get_file_section_collection(project_id).query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=["distances"])

    query_results = [{'id': UUID(id), 'similarity': 1 - distance}
                    for id, distance in zip(results['ids'][0], results['distances'][0])]

    matches = []
    with read_only_session() as session:
        for result in query_results:
            file_section = session.query(FileSection).get(result['id'])
            if file_section:
                file = session.query(File).options(joinedload(File.file_sections)).get(file_section.file_id)
                final_result = MatchResult(
                    path=file.path,
                    similarity=result['similarity'],
                    content=file_section.content
                )
                matches.append(final_result)
    return matches
