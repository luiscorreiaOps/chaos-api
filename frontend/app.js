const API_BASE = '';

async function updateStatus() {
    try {
        const response = await fetch('/chaos/status');
        const status = await response.json();

        document.querySelectorAll('.control-block').forEach(block => {
            const chaosType = block.getAttribute('data-chaos');
            const badge = block.querySelector('.status-badge');
            const statusValue = document.getElementById(`status-${chaosType}`);

            if (status[chaosType]) {
                badge.textContent = 'Ativo';
                badge.classList.remove('status-inactive');
                badge.classList.add('status-active');
                if (statusValue) {
                    statusValue.textContent = 'Ativo';
                    statusValue.classList.add('active');
                }
            } else {
                badge.textContent = 'Inativo';
                badge.classList.remove('status-active');
                badge.classList.add('status-inactive');
                if (statusValue) {
                    statusValue.textContent = 'Inativo';
                    statusValue.classList.remove('active');
                }
            }
        });
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
    }
}

setInterval(updateStatus, 2000);
updateStatus();

//CPU Stress
const cpuIntensity = document.getElementById('cpu-intensity');
const cpuValue = document.getElementById('cpu-value');
const cpuDuration = document.getElementById('cpu-duration');
const cpuDurationValue = document.getElementById('cpu-duration-value');
const cpuStart = document.getElementById('cpu-start');
const cpuStop = document.getElementById('cpu-stop');

cpuIntensity.addEventListener('input', () => {
    cpuValue.textContent = cpuIntensity.value + '%';
});

cpuDuration.addEventListener('input', () => {
    cpuDurationValue.textContent = cpuDuration.value + 's';
});

cpuStart.addEventListener('click', async () => {
    await fetch('/chaos/cpu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            percent: parseFloat(cpuIntensity.value),
            duration: parseInt(cpuDuration.value)
        })
    });
    updateStatus();
});

cpuStop.addEventListener('click', async () => {
    await fetch('/chaos/cpu/stop', { method: 'POST' });
    updateStatus();
});

//Memory Leak
const memLimit = document.getElementById('mem-limit');
const memValue = document.getElementById('mem-value');
const memRate = document.getElementById('mem-rate');
const memStart = document.getElementById('mem-start');
const memStop = document.getElementById('mem-stop');

memLimit.addEventListener('input', () => {
    memValue.textContent = memLimit.value + ' MB';
});

memStart.addEventListener('click', async () => {
    await fetch('/chaos/memory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            megabytes: parseInt(memLimit.value),
            rate: memRate.value
        })
    });
    updateStatus();
});

memStop.addEventListener('click', async () => {
    await fetch('/chaos/memory/stop', { method: 'POST' });
    updateStatus();
});

//Latency
const latencyDelay = document.getElementById('latency-delay');
const latencyValue = document.getElementById('latency-value');
const latencyJitter = document.getElementById('latency-jitter');
const latencyStart = document.getElementById('latency-start');
const latencyStop = document.getElementById('latency-stop');

latencyDelay.addEventListener('input', () => {
    latencyValue.textContent = latencyDelay.value + ' ms';
});

latencyStart.addEventListener('click', async () => {
    await fetch('/chaos/latency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            delay_ms: parseInt(latencyDelay.value),
            jitter: latencyJitter.checked
        })
    });
    updateStatus();
});

latencyStop.addEventListener('click', async () => {
    await fetch('/chaos/latency/clear', { method: 'POST' });
    updateStatus();
});

// HTTP Errors
const errorCode = document.getElementById('error-code');
const errorProbability = document.getElementById('error-probability');
const errorValue = document.getElementById('error-value');
const errorsStart = document.getElementById('errors-start');
const errorsStop = document.getElementById('errors-stop');

errorProbability.addEventListener('input', () => {
    errorValue.textContent = errorProbability.value + '%';
});

errorsStart.addEventListener('click', async () => {
    await fetch('/chaos/errors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            code: parseInt(errorCode.value),
            percentage: parseFloat(errorProbability.value)
        })
    });
    updateStatus();
});

errorsStop.addEventListener('click', async () => {
    await fetch('/chaos/errors/clear', { method: 'POST' });
    updateStatus();
});

//I/O Stress
const ioSpeed = document.getElementById('io-speed');
const ioOps = document.getElementById('io-ops');
const ioValue = document.getElementById('io-value');
const ioStart = document.getElementById('io-start');
const ioStop = document.getElementById('io-stop');

ioOps.addEventListener('input', () => {
    ioValue.textContent = ioOps.value;
});

ioStart.addEventListener('click', async () => {
    await fetch('/chaos/io', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            speed: ioSpeed.value,
            ops_per_second: parseInt(ioOps.value)
        })
    });
    updateStatus();
});

ioStop.addEventListener('click', async () => {
    await fetch('/chaos/io/stop', { method: 'POST' });
    updateStatus();
});

//QueueFlood
const queueUrl = document.getElementById('queue-url');
const queueName = document.getElementById('queue-name');
const queueRate = document.getElementById('queue-rate');
const queueValue = document.getElementById('queue-value');
const queueStart = document.getElementById('queue-start');
const queueStop = document.getElementById('queue-stop');
const queueHealthBadge = document.getElementById('queue-health-badge');
const queueSent = document.getElementById('queue-sent');
const queueRateValue = document.getElementById('queue-rate-value');
const queueStatsLink = document.getElementById('queue-stats-link');

queueRate.addEventListener('input', () => {
    queueValue.textContent = queueRate.value;
});

queueStart.addEventListener('click', async () => {
    await fetch('/chaos/queue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            url: queueUrl.value,
            queue_name: queueName.value,
            messages_per_second: parseInt(queueRate.value)
        })
    });
    updateQueueStats();
    updateStatus();
});

queueStop.addEventListener('click', async () => {
    await fetch('/chaos/queue/stop', { method: 'POST' });
    updateQueueStats();
    updateStatus();
});

async function updateQueueStats() {
    try {
        const response = await fetch('/chaos/queue/stats');
        const stats = await response.json();

        queueSent.textContent = stats.messages_sent;
        queueRateValue.textContent = stats.send_rate + '/s';

        if (stats.connection_status === 1) {
            queueHealthBadge.textContent = 'Conectado';
            queueHealthBadge.classList.remove('status-error');
            queueHealthBadge.classList.add('status-ok');
        } else {
            queueHealthBadge.textContent = 'Desconectado';
            queueHealthBadge.classList.remove('status-ok');
            queueHealthBadge.classList.add('status-error');
        }

        queueStatsLink.href = `${stats.queue_url}/queue/${stats.queue_name}/stats`;
    } catch (error) {
        console.error('Erro ao atualizar stats da fila:', error);
    }
}

setInterval(updateQueueStats, 1000);

// Stop All
const stopAllBtn = document.getElementById('stop-all');

stopAllBtn.addEventListener('click', async () => {
    await fetch('/chaos/stop-all', { method: 'DELETE' });
    updateStatus();
});
