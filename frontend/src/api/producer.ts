export async function startProducer(rate: number, pattern: string) {
  const res = await fetch(
    `/api/producer/start?rate=${rate}&pattern=${pattern}`,
    { method: "POST" }
  );
  return res.json();
}

export async function stopProducer() {
  const res = await fetch(`/api/producer/stop`, {
    method: "POST",
  });
  return res.json();
}

export async function getStatus() {
  const res = await fetch(`/api/producer/status`);
  return res.json();
}