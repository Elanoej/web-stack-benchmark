# Resultados — 8cpus-8gb

> **Ambiente:** 8cpus CPUs, 8 8GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 3607 | 4308 | 1584 |
| Latência média (ms) | 55.18 | 46.28 | 125.68 |
| Latência p50 (ms) | 19.69 | 40.01 | 126.69 |
| Latência p90 (ms) | 133.77 | 91.47 | 249.65 |
| Latência p95 (ms) | 220.91 | 105.18 | 291.50 |
| Latência máxima (ms) | 2501 | 1703 | 1596 |
| Total requisições | 108843 | 129480 | 47910 |
| Erros | 49.75% | 6.03% | 0.00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 2872 | 7346 | 1598 |
| Latência média (ms) | 75.13 | 29.25 | 135.67 |
| Latência p50 (ms) | 56.31 | 18.01 | 69.07 |
| Latência p90 (ms) | 180.66 | 81.14 | 373.60 |
| Latência p95 (ms) | 213.60 | 91.09 | 443.24 |
| Latência máxima (ms) | 746 | 119 | 2719 |
| Total requisições | 229749 | 587718 | 127833 |
| Erros | 0.08% | 0.11% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 1594 | 2704 | 1226 |
| Latência média (ms) | 51.68 | 16.56 | 82.78 |
| Latência p50 (ms) | 11.02 | 2.17 | 7.81 |
| Latência p90 (ms) | 167.48 | 49.76 | 366.41 |
| Latência p95 (ms) | 184.11 | 53.08 | 437.18 |
| Latência máxima (ms) | 719 | 79 | 2423 |
| Total requisições | 119637 | 202986 | 87581 |
| Erros | 0.00% | 0.00% | 0.00% |

---

## Resumo por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | spring-webflux (4308 req/s) | spring-mvc (3607 req/s) | fastapi-async (1584 req/s) |
| Ramp-up | spring-webflux (7346 req/s) | spring-mvc (2872 req/s) | fastapi-async (1598 req/s) |
| Spike | spring-webflux (2704 req/s) | spring-mvc (1594 req/s) | fastapi-async (1226 req/s) |

## Observações

- **spring-webflux** teve o maior throughput geral nesta configuração.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
