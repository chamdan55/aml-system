import { useEffect, useState } from "react";
import { startProducer, stopProducer, getStatus } from "../api/producer";

const PATTERNS = [
  { value: "normal", label: "Normal" },
  { value: "smurfing", label: "Smurfing" },
  { value: "fanout", label: "Fan-Out" },
  { value: "layering", label: "Layering" },
];

export default function ControlPanel() {
  const [rate, setRate] = useState(5);
  const [pattern, setPattern] = useState("normal");
  const [running, setRunning] = useState(false);
  const [sent, setSent] = useState(0);

  async function refresh() {
    const data = await getStatus();
    setRunning(data.running);
    setSent(data.sent);
  }

  async function onStart() {
    await startProducer(rate, pattern);
    refresh();
  }

  async function onStop() {
    await stopProducer();
    refresh();
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="panel">
      <h2>AML Generator Control</h2>
      <p className="subtle">Trigger synthetic transactions to test detection.</p>

      <label className="field">
        <span>Rate (tx/sec)</span>
        <input
          type="number"
          value={rate}
          min={1}
          onChange={(e) => setRate(Number(e.target.value))}
        />
      </label>

      <label className="field">
        <span>Pattern</span>
        <select value={pattern} onChange={(e) => setPattern(e.target.value)}>
          {PATTERNS.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </label>

      <div className="buttons">
        <button className="btn primary" onClick={onStart} disabled={running}>
          Generate
        </button>
        <button className="btn danger" onClick={onStop} disabled={!running}>
          Stop
        </button>
      </div>

      <div className="status-row">
        <span className={`status-badge ${running ? "running" : "stopped"}`}>
          <span className="pulse" />
          {running ? "Running" : "Stopped"}
        </span>
      </div>

      <div className="stats">
        <div className="stat">
          <div className="stat-label">Sent</div>
          <div className="stat-value">{sent}</div>
        </div>
        <div className="stat">
          <div className="stat-label">Pattern</div>
          <div className="stat-value">
            {PATTERNS.find((p) => p.value === pattern)?.label}
          </div>
        </div>
      </div>
    </div>
  );
}
