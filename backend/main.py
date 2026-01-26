from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import os

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

import chaos_cpu
import chaos_memory
import chaos_latency
import chaos_errors
import chaos_io
import chaos_queue
import chaos_control
import metrics


app = FastAPI(title="Chaos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.asyncio_sleep = asyncio.sleep

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

# estaticos
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


class CpuRequest(BaseModel):
    percent: float
    duration: int


class MemoryRequest(BaseModel):
    megabytes: int
    rate: str


class LatencyRequest(BaseModel):
    delay_ms: int
    jitter: bool


class ErrorConfigRequest(BaseModel):
    code: int
    percentage: float


class IORequest(BaseModel):
    speed: str
    ops_per_second: int


class QueueRequest(BaseModel):
    url: str
    queue_name: str
    messages_per_second: int


@app.middleware("http")
async def chaos_middleware(request: Request, call_next):
    await chaos_latency.apply_latency(request)

    maybe_code = chaos_errors.maybe_raise_error()
    if maybe_code is not None:
        return JSONResponse(
            status_code=maybe_code,
            content={"detail": f"Chaos error {maybe_code}"},
        )

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(frontend_path, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/chaos/cpu")
async def start_cpu(request: CpuRequest):
    chaos_cpu.start_cpu_stress(request.percent, request.duration)
    return {"status": "ok"}


@app.post("/chaos/cpu/stop")
async def stop_cpu():
    chaos_cpu.stop_cpu_stress()
    return {"status": "ok"}


@app.post("/chaos/memory")
async def start_memory(req: MemoryRequest):
    chaos_memory.start_memory_leak(req.megabytes, req.rate)
    return {"status": "ok"}


@app.post("/chaos/memory/stop")
async def stop_memory():
    chaos_memory.stop_memory_leak()
    return {"status": "ok"}


@app.post("/chaos/latency")
async def set_latency(req: LatencyRequest):
    chaos_latency.set_latency(req.delay_ms, req.jitter)
    return {"status": "ok"}


@app.post("/chaos/latency/clear")
async def clear_latency():
    chaos_latency.set_latency(0, False)
    return {"status": "ok"}


@app.post("/chaos/errors")
async def set_errors(req: ErrorConfigRequest):
    chaos_errors.set_error_config(req.code, req.percentage)
    return {"status": "ok"}


@app.post("/chaos/errors/clear")
async def clear_errors():
    chaos_errors.set_error_config(500, 0.0)
    return {"status": "ok"}


@app.post("/chaos/io")
async def start_io(req: IORequest):
    chaos_io.start_io_stress(req.ops_per_second, req.speed)
    return {"status": "ok"}


@app.post("/chaos/io/stop")
async def stop_io():
    chaos_io.stop_io_stress()
    return {"status": "ok"}


@app.post("/chaos/queue")
async def start_queue(req: QueueRequest):
    chaos_queue.start_queue_flood(req.url, req.queue_name, req.messages_per_second)
    return {"status": "ok"}


@app.post("/chaos/queue/stop")
async def stop_queue():
    chaos_queue.stop_queue_flood()
    return {"status": "ok"}


@app.get("/chaos/queue/stats")
async def queue_stats():
    return {
        "connection_status": int(metrics.chaos_queue_connection_status._value.get()),
        "messages_sent": int(metrics.chaos_queue_messages_sent_current._value.get()),
        "send_rate": round(metrics.chaos_queue_send_rate._value.get(), 2),
        "queue_url": chaos_queue.queue_config["url"],
        "queue_name": chaos_queue.queue_config["queue_name"]
    }


@app.get("/chaos/status")
async def status():
    return chaos_control.get_state()


@app.delete("/chaos/stop-all")
async def stop_all():
    chaos_cpu.stop_cpu_stress()
    chaos_memory.stop_memory_leak()
    chaos_latency.set_latency(0, False)
    chaos_errors.set_error_config(500, 0.0)
    chaos_io.stop_io_stress()
    chaos_queue.stop_queue_flood()
    chaos_control.stop_all()
    return {"status": "stopped"}


@app.get("/metrics")
async def metrics_endpoint():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
async def health():
    return {"status": "ok"}
