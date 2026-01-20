import threading
import time
from typing import Optional

import metrics
import chaos_control

_cpu_thread: Optional[threading.Thread] = None
_cpu_stop_event = threading.Event()

def _cpu_worker(target_percent: float, duration: int):
    metrics.chaos_cpu_stress_active.set(1)
    metrics.chaos_cpu_target_percent.set(target_percent)
    chaos_control.set_state("cpu", True)

    end_time = time.time() + duration
    busy_fraction = max(0.0, min(target_percent / 100.0, 1.0))

    while time.time() < end_time and not _cpu_stop_event.is_set():
        start_cycle = time.time()
        busy_time = busy_fraction * 0.1
        idle_time = (1 - busy_fraction) * 0.1

        while (time.time() - start_cycle) < busy_time and not _cpu_stop_event.is_set():
            _ = 1 + 1

        if idle_time > 0:
            time.sleep(idle_time)

    metrics.chaos_cpu_stress_active.set(0)
    metrics.chaos_cpu_target_percent.set(0)
    chaos_control.set_state("cpu", False)


def start_cpu_stress(percent: float, duration: int):
    global _cpu_thread
    stop_cpu_stress()

    _cpu_stop_event.clear()
    _cpu_thread = threading.Thread(
        target=_cpu_worker,
        args=(percent, duration),
        daemon=True,
    )
    _cpu_thread.start()


def stop_cpu_stress():
    _cpu_stop_event.set()
    metrics.chaos_cpu_stress_active.set(0)
    metrics.chaos_cpu_target_percent.set(0)
    chaos_control.set_state("cpu", False)
