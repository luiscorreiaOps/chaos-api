from prometheus_client import Counter, Gauge

chaos_cpu_stress_active = Gauge("chaos_cpu_stress_active", "CPU stress active (0/1)")
chaos_cpu_target_percent = Gauge("chaos_cpu_target_percent", "Target CPU percentage")
chaos_memory_allocated_bytes = Gauge("chaos_memory_allocated_bytes", "Total allocated memory for chaos in bytes")
chaos_latency_ms = Gauge("chaos_latency_ms", "Artificial latency in milliseconds")
chaos_http_errors_total = Counter("chaos_http_errors_total", "Total HTTP errors generated", ["code"])
chaos_io_operations_total = Counter("chaos_io_operations_total", "Total I/O operations performed", ["type"])
chaos_active_scenarios = Gauge("chaos_active_scenarios", "Number of active chaos scenarios")
