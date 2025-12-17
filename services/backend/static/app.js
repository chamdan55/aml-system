async function start() {
  await fetch("/api/producer/start?rate=5", { method: "POST" });
  refresh();
}

async function stop() {
  await fetch("/api/producer/stop", { method: "POST" });
  refresh();
}

async function refresh() {
  const res = await fetch("/api/producer/status");
  const data = await res.json();

  const statusEl = document.getElementById("status");
  statusEl.textContent = "Status: " + (data.running ? "RUNNING" : "STOPPED");
  statusEl.className = data.running ? "running" : "stopped";

  document.getElementById("sent").textContent = "Sent: " + data.sent;
}

// auto refresh tiap 1 detik
setInterval(refresh, 1000);
refresh();