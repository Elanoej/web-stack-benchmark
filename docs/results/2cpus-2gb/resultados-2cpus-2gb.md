# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. FastAPI com 3 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 11139 | 669 | 896 | 1798 |
| Latência média (ms) | 17.86 | 297.73 | 220.82 | 110.10 |
| Latência p50 (ms) | 23.91 | 294.83 | 15.59 | 18.49 |
| Latência p90 (ms) | 27.92 | 590.42 | 694.66 | 330.27 |
| Latência p95 (ms) | 29.06 | 896.03 | 1205.87 | 488.80 |
| Latência máxima (ms) | 124 | 2685 | 10199 | 3363 |
| Total requisições | 334557 | 20319 | 27435 | 54834 |
| Erros | 0,00% | 0,00% | 68.48% | 57.10% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 10897 | 2094 | 1185 | 1055 |
| Latência média (ms) | 19.70 | 103.14 | 182.89 | 206.35 |
| Latência p50 (ms) | 12.13 | 102.65 | 132.93 | 101.87 |
| Latência p90 (ms) | 52.40 | 226.60 | 394.50 | 554.22 |
| Latência p95 (ms) | 58.88 | 267.44 | 510.32 | 720.06 |
| Latência máxima (ms) | 152 | 362 | 2023 | 4595 |
| Total requisições | 871746 | 167520 | 94776 | 84429 |
| Erros | 0.05% | 0,00% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 3346 | 1631 | 1659 | 938 |
| Latência média (ms) | 6.96 | 49.85 | 48.36 | 113.26 |
| Latência p50 (ms) | 2.20 | 1.62 | 10.43 | 9.55 |
| Latência p90 (ms) | 19.41 | 211.60 | 152.88 | 503.99 |
| Latência p95 (ms) | 22.89 | 223.21 | 163.18 | 656.54 |
| Latência máxima (ms) | 56 | 285 | 575 | 5665 |
| Total requisições | 251178 | 122370 | 124470 | 70374 |
| Erros | 0,00% | 0,00% | 0,00% | 0.03% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (11139 req/s) | FastAPI Async (1798 req/s) | Spring MVC (896 req/s) | Spring WebFlux (669 req/s) |
| Ramp-up | Go + Gin (10897 req/s) | Spring WebFlux (2094 req/s) | Spring MVC (1185 req/s) | FastAPI Async (1055 req/s) |
| Spike | Go + Gin (3346 req/s) | Spring MVC (1659 req/s) | Spring WebFlux (1631 req/s) | FastAPI Async (938 req/s) |

## Observações

- **Go + Gin** teve o maior throughput geral em 2cpus-2gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin** (11139 req/s), menor p95 = **Go + Gin** (29.06 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin** (10897 req/s), menor p95 = **Go + Gin** (58.88 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin** (3346 req/s), menor p95 = **Go + Gin** (22.89 ms)
