const apiBase = "";

//helpers

function $(id) {
    return document.getElementById(id);
}

function updateStatusFromApi() {
    fetch(apiBase + "/chaos/status")
        .then(res => res.json())
        .then(status => {
            $("status-cpu").textContent = status.cpu ? "Ativo" : "Inativo";
            $("status-memory").textContent = status.memory ? "Ativo" : "Inativo";
            $("status-latency").textContent = status.latency ? "Ativo" : "Inativo";
            $("status-errors").textContent = status.errors ? "Ativo" : "Inativo";
            $("status-io").textContent = status.io ? "Ativo" : "Inativo";

            document.querySelectorAll(".control-block").forEach(block => {
                const name = block.getAttribute("data-chaos");
                const badge = block.querySelector(".status-badge");
                const active = status[name];
                if (active) {
                    badge.textContent = "Ativo";
                    badge.classList.remove("status-inactive");
                    badge.classList.add("status-active");
                } else {
                    badge.textContent = "Inativo";
                    badge.classList.remove("status-active");
                    badge.classList.add("status-inactive");
                }
            });
        })
        .catch(() => {
            //silencioso
        });
}

//sliders display

$("cpu-intensity").addEventListener("input", e => {
    $("cpu-value").textContent = e.target.value + "%";
});

$("cpu-duration").addEventListener("input", e => {
    $("cpu-duration-value").textContent = e.target.value + "s";
});

$("mem-limit").addEventListener("input", e => {
    $("mem-value").textContent = e.target.value + " MB";
});

$("latency-delay").addEventListener("input", e => {
    $("latency-value").textContent = e.target.value + " ms";
});

$("error-probability").addEventListener("input", e => {
    $("error-value").textContent = e.target.value + "%";
});

$("io-ops").addEventListener("input", e => {
    $("io-value").textContent = e.target.value;
});

//CPU controls

$("cpu-start").addEventListener("click", () => {
    const percent = parseFloat($("cpu-intensity").value);
    const duration = parseInt($("cpu-duration").value, 10);
    fetch(apiBase + "/chaos/cpu", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({percent, duration})
    }).then(updateStatusFromApi);
});

$("cpu-stop").addEventListener("click", () => {
    fetch(apiBase + "/chaos/cpu/stop", {method: "POST"})
        .then(updateStatusFromApi);
});

//Memory controls

$("mem-start").addEventListener("click", () => {
    const megabytes = parseInt($("mem-limit").value, 10);
    const rate = $("mem-rate").value;
    fetch(apiBase + "/chaos/memory", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({megabytes, rate})
    }).then(updateStatusFromApi);
});

$("mem-stop").addEventListener("click", () => {
    fetch(apiBase + "/chaos/memory/stop", {method: "POST"})
        .then(updateStatusFromApi);
});

//Latency controls

$("latency-start").addEventListener("click", () => {
    const delay_ms = parseInt($("latency-delay").value, 10);
    const jitter = $("latency-jitter").checked;
    fetch(apiBase + "/chaos/latency", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({delay_ms, jitter})
    }).then(updateStatusFromApi);
});

$("latency-stop").addEventListener("click", () => {
    fetch(apiBase + "/chaos/latency/clear", {method: "POST"})
        .then(updateStatusFromApi);
});

//Errors controls

$("errors-start").addEventListener("click", () => {
    const code = parseInt($("error-code").value, 10);
    const percentage = parseFloat($("error-probability").value);
    fetch(apiBase + "/chaos/errors", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code, percentage})
    }).then(updateStatusFromApi);
});

$("errors-stop").addEventListener("click", () => {
    fetch(apiBase + "/chaos/errors/clear", {method: "POST"})
        .then(updateStatusFromApi);
});

//IO controls

$("io-start").addEventListener("click", () => {
    const speed = $("io-speed").value;
    const ops_per_second = parseInt($("io-ops").value, 10);
    fetch(apiBase + "/chaos/io", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({speed, ops_per_second})
    }).then(updateStatusFromApi);
});

$("io-stop").addEventListener("click", () => {
    fetch(apiBase + "/chaos/io/stop", {method: "POST"})
        .then(updateStatusFromApi);
});

// stop all

$("stop-all").addEventListener("click", () => {
    fetch(apiBase + "/chaos/stop-all", {method: "DELETE"})
        .then(updateStatusFromApi);
});

// atualiza

updateStatusFromApi();
setInterval(updateStatusFromApi, 3000);
