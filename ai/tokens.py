
import tiktoken


def count_tokens(text) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode_ordinary(str(text)))
