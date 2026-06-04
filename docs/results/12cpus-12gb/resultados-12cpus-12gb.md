# Resultados — 12cpus-12gb

> **Ambiente:** 12cpus CPUs, 12 12GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 3831 | 6039 | 1599 |
| Latência média (ms) | 51.93 | 32.98 | 124.58 |
| Latência p50 (ms) | 20.22 | 32.24 | 133.85 |
| Latência p90 (ms) | 125.28 | 61.40 | 240.46 |
| Latência p95 (ms) | 207.14 | 74.69 | 297.71 |
| Latência máxima (ms) | 1885 | 1563 | 1451 |
| Total requisições | 115626 | 181434 | 48327 |
| Erros | 49.37% | 4.99% | 0.00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 2939 | 8943 | 1629 |
| Latência média (ms) | 73.42 | 23.99 | 133.05 |
| Latência p50 (ms) | 56.50 | 14.94 | 65.10 |
| Latência p90 (ms) | 175.46 | 65.24 | 371.21 |
| Latência p95 (ms) | 201.96 | 74.12 | 445.29 |
| Latência máxima (ms) | 665 | 116 | 2682 |
| Total requisições | 235110 | 715482 | 130317 |
| Erros | 0.01% | 0.22% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 1610 | 3017 | 1089 |
| Latência média (ms) | 50.83 | 11.37 | 91.95 |
| Latência p50 (ms) | 10.92 | 2.20 | 8.22 |
| Latência p90 (ms) | 164.15 | 32.45 | 371.76 |
| Latência p95 (ms) | 178.90 | 35.94 | 449.91 |
| Latência máxima (ms) | 724 | 60 | 2678 |
| Total requisições | 120816 | 226341 | 81744 |
| Erros | 0.00% | 0.00% | 0.00% |

---

## Resumo por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | spring-webflux (6039 req/s) | spring-mvc (3831 req/s) | fastapi-async (1599 req/s) |
| Ramp-up | spring-webflux (8943 req/s) | spring-mvc (2939 req/s) | fastapi-async (1629 req/s) |
| Spike | spring-webflux (3017 req/s) | spring-mvc (1610 req/s) | fastapi-async (1089 req/s) |

## Observações

- **spring-webflux** teve o maior throughput geral nesta configuração.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
