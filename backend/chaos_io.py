import threading
import time
import os
from typing import Optional

import metrics
import chaos_control

_io_thread: Optional[threading.Thread] = None
_io_stop_event = threading.Event()
_temp_file = "chaos_io_temp.dat"

def _speed_to_sleep(speed: str) -> float:
    if speed == "low":
        return 0.2
    if speed == "high":
        return 0.01
    return 0.05


def _io_worker(ops_per_sec: int, speed: str):
    chaos_control.set_state("io", True)
    sleep_time = _speed_to_sleep(speed)
    data = b"x" * 4096

    while not _io_stop_event.is_set():
        with open(_temp_file, "ab") as f:
            f.write(data)
        metrics.chaos_io_operations_total.labels(type="write").inc()

        try:
            with open(_temp_file, "rb") as f:
                _ = f.read(4096)
            metrics.chaos_io_operations_total.labels(type="read").inc()
        except FileNotFoundError:
            pass

        time.sleep(sleep_time)


def start_io_stress(ops_per_sec: int, speed: str):
    global _io_thread
    stop_io_stress()
    _io_stop_event.clear()
    _io_thread = threading.Thread(
        target=_io_worker,
        args=(ops_per_sec, speed),
        daemon=True,
    )
    _io_thread.start()


def stop_io_stress():
    _io_stop_event.set()
    chaos_control.set_state("io", False)
    try:
        if os.path.exists(_temp_file):
            os.remove(_temp_file)
    except OSError:
        pass
