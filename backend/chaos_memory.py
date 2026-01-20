import threading
import time
from typing import Optional, List

import metrics
import chaos_control

_mem_thread: Optional[threading.Thread] = None
_mem_stop_event = threading.Event()
_allocated: List[bytearray] = []

def _rate_to_sleep(rate: str) -> float:
    if rate == "slow":
        return 0.5
    elif rate == "fast":
        return 0.05
    return 0.2


def _memory_worker(limit_mb: int, rate: str):
    global _allocated
    _allocated = []
    chaos_control.set_state("memory", True)

    sleep_time = _rate_to_sleep(rate)
    target_bytes = limit_mb * 1024 * 1024

    while not _mem_stop_event.is_set():
        current_bytes = len(_allocated) * 1024 * 1024
        if current_bytes >= target_bytes:
            break

        chunk = bytearray(1 * 1024 * 1024)
        _allocated.append(chunk)
        current = len(_allocated) * 1024 * 1024
        metrics.chaos_memory_allocated_bytes.set(current)
        time.sleep(sleep_time)

    chaos_control.set_state("memory", False)


def start_memory_leak(limit_mb: int, rate: str):
    global _mem_thread
    stop_memory_leak()
    _mem_stop_event.clear()
    _mem_thread = threading.Thread(
        target=_memory_worker,
        args=(limit_mb, rate),
        daemon=True,
    )
    _mem_thread.start()


def stop_memory_leak():
    global _allocated
    _mem_stop_event.set()
    _allocated = []
    metrics.chaos_memory_allocated_bytes.set(0)
    chaos_control.set_state("memory", False)
