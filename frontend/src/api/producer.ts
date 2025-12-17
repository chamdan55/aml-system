const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function startProducer(rate: number, pattern: string) {
  const res = await fetch(
    `${BASE_URL}/api/producer/start?rate=${rate}&pattern=${pattern}`,
    { method: "POST" }
  );
  return res.json();
}

export async function stopProducer() {
  const res = await fetch(`${BASE_URL}/api/producer/stop`, {
    method: "POST",
  });
  return res.json();
}

export async function getStatus() {
  const res = await fetch(`${BASE_URL}/api/producer/status`);
  return res.json();
}
