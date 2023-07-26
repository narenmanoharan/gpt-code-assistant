import fnmatch
import logging
import os
from hashlib import sha256
from tqdm import tqdm
from typing import List

from pydantic import BaseModel

from ai.tokens import count_tokens
from data.projects import Project


class Chunk(BaseModel):
    checksum: str
    file_path: str
    sections: List[str]

class ChunkResult(BaseModel):
    chunks: List[Chunk]
    indexed: int
    skipped: int

SOURCE_MAX_TOKEN = 700
MARKDOWN_MAX_TOKEN = 1000

def source_files(project: Project) -> List[str]:
    logging.debug(f"Start finding source files in {project.name}...")
    ignore_patterns = [
        # Configuration files/dirs
        ".git", ".svn", ".hg", ".vscode", ".idea", ".eclipse", ".docker", ".github", ".gitlab", ".circleci",
        # Cache and temporary files/dirs
        "*cache*", "__pycache__", "*.pyc", ".DS_Store",
        # Binary files
        "*.bin", "*.o", "*.so", "*.lib", "*.dll", "*.exe", "*.class", "*.jar",
        # Package and lock files
        "package-lock.json", "*.lock",
        # Log files
        "*.log",
        # Image files
        "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tiff",
        # Node modules
        "node_modules",
    ]
    file_paths = []
    for dirpath, dirnames, filenames in tqdm(os.walk(project.path), desc="Walking through project directories"):
        # Exclude directories and files matched by ignore_patterns
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        filenames[:] = [f for f in filenames if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns)]
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            file_paths.append(file_path)
    logging.debug(f"Total number of files: {len(file_paths)}")
    return file_paths

def chunk_source_files(src_files: List[str]) -> ChunkResult:
    chunks = []
    skipped = 0
    for file_path in tqdm(src_files, desc="Processing source files"):
        _, file_extension = os.path.splitext(file_path)
        if not file_extension:
            logging.debug(f"File {file_path} has no extension, skipping...")
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                checksum = sha256(content.encode("utf-8")).hexdigest()
                sections = chunk_source(content)
                if len(sections) > 0:
                    chunk = Chunk(checksum=checksum, file_path=file_path, sections=sections)
                    chunks.append(chunk)
        except FileNotFoundError:
            logging.debug(f"File {file_path} does not exist, skipping...")
            skipped += 1
        except UnicodeDecodeError:
            logging.debug(f"File {file_path} could not be read as text, skipping...")
            skipped += 1
    logging.debug(f"Total number of chunks: {len(chunks)}")
    return ChunkResult(chunks=chunks, indexed=len(src_files) - skipped, skipped=skipped)


def chunk_source(content: str) -> List[str]:
    lines = [line for line in content.split("\n")]
    chunks = []
    current_chunk = ""
    token_count = 0
    for line in lines:
        current_chunk += line + "\n"
        token_count += count_tokens(line)
        if token_count >= SOURCE_MAX_TOKEN:
            chunks.append(current_chunk)
            current_chunk = ""
            token_count = 0
    if current_chunk != "":
        chunks.append(current_chunk)
    return chunks
