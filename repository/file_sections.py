

from data.database import read_write_session
from data.file_sections import FileSection


def create_file_sections(file_id: str, content: str) -> str:
    with read_write_session() as session:
        file_section = session.query(FileSection).filter(FileSection.file_id == file_id).first()
        if not file_section:
            file_section = FileSection(file_id=file_id, content=content)
            session.add(file_section)
        session.commit()
        return file_section.id
