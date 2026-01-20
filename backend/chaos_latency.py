import random
from fastapi import Request

import metrics
import chaos_control

latency_config = {
    "delay_ms": 0,
    "jitter": False,
}

def set_latency(delay_ms: int, jitter: bool):
    latency_config["delay_ms"] = max(delay_ms, 0)
    latency_config["jitter"] = jitter
    metrics.chaos_latency_ms.set(delay_ms)
    chaos_control.set_state("latency", delay_ms > 0)


async def apply_latency(request: Request):
    delay_ms = latency_config["delay_ms"]
    if delay_ms <= 0:
        return
    delay = delay_ms / 1000.0
    if latency_config["jitter"]:
        jitter_factor = random.uniform(0.5, 1.5)
        delay *= jitter_factor
    await request.app.state.asyncio_sleep(delay)
