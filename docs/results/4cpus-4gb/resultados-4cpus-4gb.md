# Resultados — 4cpus-4gb

> **Ambiente:** 4cpus CPUs, 4 4GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 2895 | 2000 | 1583 |
| Latência média (ms) | 68.75 | 99.75 | 125.80 |
| Latência p50 (ms) | 19.79 | 104.13 | 135.58 |
| Latência p90 (ms) | 175.44 | 188.97 | 248.15 |
| Latência p95 (ms) | 297.97 | 221.86 | 292.52 |
| Latência máxima (ms) | 5191 | 2633 | 1612 |
| Total requisições | 87456 | 60213 | 47847 |
| Erros | 63.09% | 15.86% | 0.00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 2886 | 4470 | 1630 |
| Latência média (ms) | 74.79 | 48.20 | 133.05 |
| Latência p50 (ms) | 57.51 | 30.25 | 65.76 |
| Latência p90 (ms) | 178.26 | 131.50 | 370.32 |
| Latência p95 (ms) | 205.43 | 151.28 | 464.06 |
| Latência máxima (ms) | 952 | 189 | 2654 |
| Total requisições | 230883 | 357624 | 130413 |
| Erros | 0.02% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 1605 | 2067 | 1158 |
| Latência média (ms) | 51.10 | 32.08 | 89.32 |
| Latência p50 (ms) | 10.80 | 1.87 | 9.14 |
| Latência p90 (ms) | 165.70 | 115.00 | 366.18 |
| Latência p95 (ms) | 183.41 | 119.68 | 442.60 |
| Latência máxima (ms) | 673 | 148 | 2344 |
| Total requisições | 120465 | 155109 | 83026 |
| Erros | 0.00% | 0.00% | 0.00% |

---

## Resumo por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | spring-mvc (2895 req/s) | spring-webflux (2000 req/s) | fastapi-async (1583 req/s) |
| Ramp-up | spring-webflux (4470 req/s) | spring-mvc (2886 req/s) | fastapi-async (1630 req/s) |
| Spike | spring-webflux (2067 req/s) | spring-mvc (1605 req/s) | fastapi-async (1158 req/s) |

## Observações

- **spring-webflux** teve o maior throughput geral nesta configuração.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **spring-mvc**, menor p95 = **spring-webflux**
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
