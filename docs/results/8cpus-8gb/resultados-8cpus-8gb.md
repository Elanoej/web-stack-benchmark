# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. FastAPI com 9 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 12599 | 4235 | 2464 | 2287 |
| Latência média (ms) | 15.77 | 47.07 | 80.79 | 86.85 |
| Latência p50 (ms) | 15.40 | 40.13 | 90.23 | 19.28 |
| Latência p90 (ms) | 17.38 | 92.96 | 191.14 | 254.68 |
| Latência p95 (ms) | 18.35 | 103.94 | 218.70 | 324.15 |
| Latência máxima (ms) | 612 | 1141 | 1571 | 2001 |
| Total requisições | 378408 | 127269 | 74358 | 69420 |
| Erros | 0,00% | 0,00% | 0,00% | 43.37% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 12613 | 7629 | 3062 | 1626 |
| Latência média (ms) | 16.99 | 28.17 | 70.46 | 133.36 |
| Latência p50 (ms) | 14.87 | 18.02 | 55.46 | 66.54 |
| Latência p90 (ms) | 35.38 | 78.25 | 166.06 | 350.43 |
| Latência p95 (ms) | 37.80 | 87.67 | 189.63 | 454.96 |
| Latência máxima (ms) | 85 | 134 | 650 | 2626 |
| Total requisições | 1009068 | 610350 | 244989 | 130056 |
| Erros | 0,00% | 0.12% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 3652 | 2792 | 1643 | 1237 |
| Latência média (ms) | 3.59 | 15.02 | 49.10 | 76.85 |
| Latência p50 (ms) | 2.48 | 1.88 | 10.69 | 5.98 |
| Latência p90 (ms) | 7.93 | 46.02 | 156.69 | 363.17 |
| Latência p95 (ms) | 9.37 | 49.11 | 167.95 | 409.51 |
| Latência máxima (ms) | 23 | 81 | 518 | 2979 |
| Total requisições | 274044 | 209427 | 123393 | 92904 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (12599 req/s) | Spring WebFlux (4235 req/s) | Spring MVC (2464 req/s) | FastAPI Async (2287 req/s) |
| Ramp-up | Go + Gin (12613 req/s) | Spring WebFlux (7629 req/s) | Spring MVC (3062 req/s) | FastAPI Async (1626 req/s) |
| Spike | Go + Gin (3652 req/s) | Spring WebFlux (2792 req/s) | Spring MVC (1643 req/s) | FastAPI Async (1237 req/s) |

## Observações

- **Go + Gin** teve o maior throughput geral em 8cpus-8gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin** (12599 req/s), menor p95 = **Go + Gin** (18.35 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin** (12613 req/s), menor p95 = **Go + Gin** (37.80 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin** (3652 req/s), menor p95 = **Go + Gin** (9.37 ms)
