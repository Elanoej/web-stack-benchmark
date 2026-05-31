# Benchmark FastAPI Async

**Data:** 31/05/2026 17:57
**Stack:** FastAPI + SQLAlchemy async + asyncpg + PostgreSQL
**Execucoes por cenario:** 5
**Metrica exibida:** media aritmetica das execucoes

## Resultados

| Metrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| avg (ms) | 350.30 | 381.63 | 358.66 |
| med / p50 (ms) | 316.13 | 82.66 | 65.56 |
| p90 (ms) | 884.40 | 1127.82 | 1223.59 |
| p95 (ms) | 965.06 | 1328.59 | 1344.74 |
| throughput (req/s) | 566 | 577 | 358 |
| erro (%) | 0.00% | 0.00% | 0.53% |
