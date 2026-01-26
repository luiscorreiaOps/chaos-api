import threading
import time
import requests
from typing import Optional

import metrics
import chaos_control

_queue_thread: Optional[threading.Thread] = None
_queue_stop_event = threading.Event()
_messages_sent = 0
_last_update_time = time.time()

queue_config = {
    "url": "http://localhost:8080",
    "queue_name": "chaos-test",
    "messages_per_second": 10,
}


def set_queue_config(url: str, queue_name: str, messages_per_second: int):
    queue_config["url"] = url
    queue_config["queue_name"] = queue_name
    queue_config["messages_per_second"] = max(1, messages_per_second)


def _ensure_queue_exists():
    try:
        requests.post(
            f"{queue_config['url']}/queue/{queue_config['queue_name']}",
            timeout=2
        )
        metrics.chaos_queue_connection_status.set(1)
        return True
    except Exception:
        metrics.chaos_queue_connection_status.set(0)
        return False


def _queue_worker():
    global _messages_sent, _last_update_time

    chaos_control.set_state("queue", True)

    if not _ensure_queue_exists():
        chaos_control.set_state("queue", False)
        return

    _messages_sent = 0
    _last_update_time = time.time()
    sleep_time = 1.0 / queue_config["messages_per_second"]
    counter = 0

    while not _queue_stop_event.is_set():
        try:
            counter += 1
            payload = {
                "chaos_id": counter,
                "timestamp": time.time(),
                "data": "x" * 100
            }

            response = requests.post(
                f"{queue_config['url']}/queue/{queue_config['queue_name']}/send",
                json=payload,
                timeout=2
            )

            if response.status_code == 200:
                _messages_sent += 1
                metrics.chaos_queue_messages_sent_total.inc()
                metrics.chaos_queue_messages_sent_current.set(_messages_sent)
                metrics.chaos_queue_connection_status.set(1)

                now = time.time()
                elapsed = now - _last_update_time
                if elapsed >= 1.0:
                    rate = _messages_sent / elapsed
                    metrics.chaos_queue_send_rate.set(rate)
                    _messages_sent = 0
                    _last_update_time = now
            else:
                metrics.chaos_queue_errors_total.inc()
                metrics.chaos_queue_connection_status.set(0)

        except Exception as e:
            metrics.chaos_queue_errors_total.inc()
            metrics.chaos_queue_connection_status.set(0)

        time.sleep(sleep_time)

    metrics.chaos_queue_connection_status.set(0)
    metrics.chaos_queue_messages_sent_current.set(0)
    metrics.chaos_queue_send_rate.set(0)
    chaos_control.set_state("queue", False)


def start_queue_flood(url: str, queue_name: str, messages_per_second: int):
    global _queue_thread
    stop_queue_flood()

    set_queue_config(url, queue_name, messages_per_second)

    _queue_stop_event.clear()
    _queue_thread = threading.Thread(
        target=_queue_worker,
        daemon=True,
    )
    _queue_thread.start()


def stop_queue_flood():
    _queue_stop_event.set()
    metrics.chaos_queue_connection_status.set(0)
    metrics.chaos_queue_messages_sent_current.set(0)
    metrics.chaos_queue_send_rate.set(0)
    chaos_control.set_state("queue", False)
