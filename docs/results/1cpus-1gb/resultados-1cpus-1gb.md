# Resultados — 1cpus-1gb

> **Ambiente:** 1cpus CPUs, 1 1GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 6354 | 2901 | 1223 |
| Latência média (ms) | 30.14 | 67.23 | 162.00 |
| Latência p50 (ms) | 18.79 | 19.08 | 20.09 |
| Latência p90 (ms) | 21.81 | 22.67 | 403.11 |
| Latência p95 (ms) | 22.88 | 23.60 | 815.20 |
| Latência máxima (ms) | 12881 | 9451 | 6400 |
| Total requisições | 211686 | 91473 | 37419 |
| Erros | 99.80% | 97.26% | 65.08% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 408 | 502 | 525 |
| Latência média (ms) | 541.61 | 437.21 | 419.72 |
| Latência p50 (ms) | 398.04 | 304.33 | 204.79 |
| Latência p90 (ms) | 1226.60 | 1093.05 | 1183.77 |
| Latência p95 (ms) | 1513.76 | 1195.49 | 1370.68 |
| Latência máxima (ms) | 4816 | 1412 | 6695 |
| Total requisições | 32628 | 40134 | 41979 |
| Erros | 0.00% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | spring-mvc | spring-webflux | fastapi-async |
|---|------|---|---|
| Throughput (req/s) | 680 | 1080 | 467 |
| Latência média (ms) | 221.21 | 93.73 | 268.47 |
| Latência p50 (ms) | 84.31 | 2.00 | 74.82 |
| Latência p90 (ms) | 705.70 | 531.71 | 1182.09 |
| Latência p95 (ms) | 886.20 | 683.82 | 1480.38 |
| Latência máxima (ms) | 3212 | 793 | 6608 |
| Total requisições | 37328 | 81099 | 35028 |
| Erros | 0.41% | 0.17% | 0.13% |

---

## Resumo por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | spring-mvc (6354 req/s) | spring-webflux (2901 req/s) | fastapi-async (1223 req/s) |
| Ramp-up | fastapi-async (525 req/s) | spring-webflux (502 req/s) | spring-mvc (408 req/s) |
| Spike | spring-webflux (1080 req/s) | spring-mvc (680 req/s) | fastapi-async (467 req/s) |

## Observações

- **spring-mvc** teve o maior throughput geral nesta configuração.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **spring-mvc**, menor p95 = **spring-mvc**
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **fastapi-async**, menor p95 = **spring-webflux**
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **spring-webflux**, menor p95 = **spring-webflux**
