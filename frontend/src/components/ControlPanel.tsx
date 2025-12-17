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

      <label>
        Rate (tx/sec):
        <input
          type="number"
          value={rate}
          min={1}
          onChange={(e) => setRate(Number(e.target.value))}
        />
      </label>

      <label>
        Pattern:
        <select value={pattern} onChange={(e) => setPattern(e.target.value)}>
          {PATTERNS.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </label>

      <div className="buttons">
        <button onClick={onStart} disabled={running}>
          Generate
        </button>
        <button onClick={onStop} disabled={!running}>
          Stop
        </button>
      </div>

      <p>Status: <b>{running ? "RUNNING" : "STOPPED"}</b></p>
      <p>Sent: {sent}</p>
    </div>
  );
}
