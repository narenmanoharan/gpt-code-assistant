

from typing import Optional

from data.chroma import delete_file_section_embeddings
from data.database import read_only_session, read_write_session
from data.file_sections import FileSection
from data.files import File


def create_or_update_file(project_id: str, index_id: str, file_path: str, checksum: str) -> str:
    with read_write_session() as session:
        file = session.query(File).filter(File.path == file_path).first()
        if file:
            file.project_id = project_id
            file.index_id = index_id
            file.checksum = checksum
        else:
            file = File(
                project_id=project_id,
                index_id=index_id,
                path=file_path,
                checksum=checksum,
            )
            session.add(file)
        session.commit()
        return file.id

def get_file(file_path) -> Optional[File]:
    with read_only_session() as session:
        return session.query(File).filter(File.path == file_path).first()


def delete_files_from_previous_index(project_id: str, current_index_id: str):
    with read_write_session() as session:
        files = session.query(File).filter(File.project_id == project_id, File.index_id != current_index_id).all()
        file_ids = [file.id for file in files]
        file_sections = session.query(FileSection).filter(FileSection.file_id.in_(file_ids)).all()
        file_section_ids = [file_section.id for file_section in file_sections]
        session.query(File).filter(File.id.in_(file_ids)).delete(synchronize_session=False)
        for file_section_id in file_section_ids:
            delete_file_section_embeddings(project_id, file_section_id)
        session.query(FileSection).filter(FileSection.id.in_(file_section_ids)).delete(synchronize_session=False)
        session.commit()
