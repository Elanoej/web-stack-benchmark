const STACK    = __ENV.STACK    || "unknown";
const SCENARIO = __ENV.SCENARIO || "unknown";
const CFG      = __ENV.CFG      || "unknown";

export function handleSummary(data) {
  const duration = data.metrics.http_req_duration;
  const reqs     = data.metrics.http_reqs;
  const failed   = data.metrics.http_req_failed;

  const throughput = reqs?.values?.rate          ?? 0;
  const avg        = duration?.values?.avg        ?? 0;
  const med        = duration?.values?.med        ?? 0;
  const p90        = duration?.values?.["p(90)"]  ?? 0;
  const p95        = duration?.values?.["p(95)"]  ?? 0;
  const p99        = duration?.values?.["p(99)"]  ?? 0;
  const max        = duration?.values?.max        ?? 0;
  const total      = reqs?.values?.count          ?? 0;
  const errorRate  = failed?.values?.rate         ?? 0;

  const result = {
    stack:           STACK,
    scenario:        SCENARIO,
    cfg:             CFG,
    throughput_rps:  parseFloat(throughput.toFixed(2)),
    avg_ms:          parseFloat(avg.toFixed(2)),
    med_ms:          parseFloat(med.toFixed(2)),
    p90_ms:          parseFloat(p90.toFixed(2)),
    p95_ms:          parseFloat(p95.toFixed(2)),
    p99_ms:          parseFloat(p99.toFixed(2)),
    max_ms:          parseFloat(max.toFixed(2)),
    total_requests:  parseFloat(total.toFixed(0)),
    error_rate_pct:  parseFloat((errorRate * 100).toFixed(2)),
  };

  const summary = `
╔══════════════════════════════════════════╗
║           RESULTADO DO BENCHMARK         ║
║  ${(STACK + " | " + SCENARIO + " | " + CFG).padEnd(40)}║
╠══════════════════════════════════════════╣
║  Throughput   : ${String(result.throughput_rps).padStart(10)} req/s          ║
║  Média        : ${String(result.avg_ms).padStart(10)} ms             ║
║  p50          : ${String(result.med_ms).padStart(10)} ms             ║
║  p90          : ${String(result.p90_ms).padStart(10)} ms             ║
║  p95          : ${String(result.p95_ms).padStart(10)} ms             ║
║  p99          : ${String(result.p99_ms).padStart(10)} ms             ║
║  Máxima       : ${String(result.max_ms).padStart(10)} ms             ║
║  Total reqs   : ${String(result.total_requests).padStart(10)}                ║
║  Erros        : ${String(result.error_rate_pct).padStart(10)} %              ║
╚══════════════════════════════════════════╝
`;

  return {
    stdout: summary,
    [`docs/v2/results/${CFG}/${STACK}/${SCENARIO}-summary.json`]: JSON.stringify(result, null, 2),
  };
}
