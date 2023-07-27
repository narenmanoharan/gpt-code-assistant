
import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value
from typing import List

from rich.console import Console
from tqdm import tqdm

from data.chroma import create_file_section_embeddings
from index.file_processor import Chunk
from repository.file_sections import create_file_sections
from repository.files import create_or_update_file, delete_files_from_previous_index

console = Console()

def create_embeddings_for_chunks(project_id: str, index_id: str, chunks: List[Chunk]):
    total_chunks = len(chunks)
    files_left = Value("i", total_chunks)
    console.print(f"Creating embeddings for {total_chunks} chunks")
    progress_bar = tqdm(total=total_chunks, desc="Indexing", position=0, leave=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        [executor.submit(index_chunks, project_id, index_id, chunk, files_left, progress_bar) for chunk in chunks]
    progress_bar.close()
    console.print("Embeddings created and files indexed.")

def index_chunks(project_id: str, index_id: str, chunk: Chunk, files_left: Value, progress_bar):
    """Function to index chunks in parallel. This happens in two phases:

    1. Create/modify/delete the files as needed in the database and wait for generating the embeddings.
    2. Generate the embeddings as necessary and store them in the local chroma db.
    """
    try:
        file_id = create_or_update_file(project_id, index_id, chunk.file_path, chunk.checksum)
        for section in chunk.sections:
            file_section_id = create_file_sections(file_id, section)
            create_file_section_embeddings(project_id, file_section_id, section)
        delete_files_from_previous_index(project_id, index_id)
    except Exception as ex:
        logging.info(f"Error occurred during embedding creation and indexing: {str(ex)}")
    finally:
        with files_left.get_lock():
            files_left.value -= 1
            progress_bar.update(1)
