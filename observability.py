from uuid import uuid4
import time


def create_trace_id():
    return str(uuid4())[:8]


def log(trace_id: str, message: str):
    print(f"[Trace:{trace_id}] {message}")


def now() -> float:
    return time.perf_counter()


def elapsed_seconds(start_time: float) -> float:
    return time.perf_counter() - start_time
