from typing import Dict
from threading import Lock
import metrics

_state_lock = Lock()
_state: Dict[str, bool] = {
    "cpu": False,
    "memory": False,
    "latency": False,
    "errors": False,
    "io": False,
    "queue" : False,
}

def set_state(name: str, active: bool) -> None:
    with _state_lock:
        if name in _state:
            _state[name] = active
        metrics.chaos_active_scenarios.set(sum(1 for v in _state.values() if v))

def get_state() -> Dict[str, bool]:
    with _state_lock:
        return dict(_state)

def stop_all() -> None:
    with _state_lock:
        for k in _state:
            _state[k] = False
        metrics.chaos_cpu_stress_active.set(0)
        metrics.chaos_cpu_target_percent.set(0)
        metrics.chaos_memory_allocated_bytes.set(0)
        metrics.chaos_latency_ms.set(0)
        metrics.chaos_active_scenarios.set(0)
