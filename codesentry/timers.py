import time
from contextlib import contextmanager
from typing import Dict, Any, Generator


@contextmanager
def timed() -> Generator[Dict[str, Any], None, None]:
    """
    Usage:
        with timed() as t:
            ... do work ...
        duration = t["duration"]
    """
    data: Dict[str, Any] = {"start": time.perf_counter(), "duration": None}
    try:
        yield data
    finally:
        data["duration"] = time.perf_counter() - data["start"]
