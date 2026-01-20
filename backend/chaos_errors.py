import random
from typing import Dict

import metrics
import chaos_control

error_config: Dict[str, float] = {
    "code": 500,
    "percentage": 0.0,
}

def set_error_config(code: int, percentage: float):
    error_config["code"] = code
    error_config["percentage"] = max(0.0, min(percentage, 100.0))
    chaos_control.set_state("errors", error_config["percentage"] > 0.0)


def maybe_raise_error():
    p = error_config["percentage"]
    if p <= 0:
        return None
    if random.random() * 100 <= p:
        code = error_config["code"]
        metrics.chaos_http_errors_total.labels(code=str(code)).inc()
        return code
    return None
