from typing import Iterable, List

def chunk_list(seq: List, size: int) -> Iterable[List]:
    """Yield successive `size`-sized chunks from seq."""
    for i in range(0, len(seq), size):
        yield seq[i:i + size]