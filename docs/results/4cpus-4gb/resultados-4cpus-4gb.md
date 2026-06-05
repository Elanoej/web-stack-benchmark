# Resultados — 4cpus-4gb

> **Ambiente:** 4cpus CPUs, 4 4GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 2049 | 2016 | 1579 |
| Latência média (ms) | 97.18 | 98.90 | 125.98 |
| Latência p50 (ms) | 98.34 | 103.25 | 91.21 |
| Latência p90 (ms) | 217.50 | 187.64 | 255.21 |
| Latência p95 (ms) | 299.62 | 209.14 | 345.08 |
| Latência máxima (ms) | 1898 | 2617 | 1603 |
| Total requisições | 61815 | 60744 | 47811 |
| Erros | 0.00% | 13.91% | 0.00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 3079 | 4400 | 1599 |
| Latência média (ms) | 70.05 | 48.96 | 135.63 |
| Latência p50 (ms) | 55.02 | 30.31 | 67.71 |
| Latência p90 (ms) | 166.10 | 135.83 | 374.33 |
| Latência p95 (ms) | 186.47 | 152.36 | 452.63 |
| Latência máxima (ms) | 597 | 193 | 2193 |
| Total requisições | 246315 | 352011 | 127917 |
| Erros | 0.01% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 1650 | 2058 | 1192 |
| Latência média (ms) | 48.75 | 32.39 | 85.97 |
| Latência p50 (ms) | 10.49 | 1.83 | 7.64 |
| Latência p90 (ms) | 157.14 | 114.81 | 366.42 |
| Latência p95 (ms) | 170.71 | 120.92 | 442.09 |
| Latência máxima (ms) | 551 | 161 | 2325 |
| Total requisições | 123828 | 154404 | 85349 |
| Erros | 0.00% | 0.00% | 0.00% |

---

## Resumo por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | spring-mvc (2049 req/s) | spring-webflux (2016 req/s) | fastapi-async (1579 req/s) |
| Ramp-up | spring-webflux (4400 req/s) | spring-mvc (3079 req/s) | fastapi-async (1599 req/s) |
| Spike | spring-webflux (2058 req/s) | spring-mvc (1650 req/s) | fastapi-async (1192 req/s) |

## Observações

- **spring-webflux** teve o maior throughput geral nesta configuração.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **spring-mvc**, menor p95 = **spring-webflux**
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
