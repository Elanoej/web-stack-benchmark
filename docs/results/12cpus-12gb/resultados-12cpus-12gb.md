# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. FastAPI com 13 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 13425 | 6507 | 2580 | 1529 |
| Latência média (ms) | 14.80 | 30.60 | 77.14 | 130.00 |
| Latência p50 (ms) | 14.52 | 29.88 | 91.27 | 99.32 |
| Latência p90 (ms) | 16.03 | 58.39 | 149.45 | 272.34 |
| Latência p95 (ms) | 16.88 | 71.46 | 218.36 | 327.46 |
| Latência máxima (ms) | 532 | 910 | 1041 | 1630 |
| Total requisições | 403134 | 195453 | 77841 | 46308 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 12856 | 9641 | 3046 | 1584 |
| Latência média (ms) | 16.67 | 22.25 | 70.84 | 137.08 |
| Latência p50 (ms) | 14.53 | 14.12 | 57.84 | 67.09 |
| Latência p90 (ms) | 34.06 | 59.17 | 165.12 | 406.67 |
| Latência p95 (ms) | 36.98 | 67.99 | 185.02 | 503.47 |
| Latência máxima (ms) | 76 | 109 | 524 | 3203 |
| Total requisições | 1028502 | 771336 | 243699 | 126702 |
| Erros | 0,00% | 0.23% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 3684 | 3171 | 1644 | 1211 |
| Latência média (ms) | 3.24 | 9.20 | 49.07 | 79.36 |
| Latência p50 (ms) | 2.22 | 2.24 | 10.86 | 6.23 |
| Latência p90 (ms) | 7.14 | 25.91 | 156.47 | 360.01 |
| Latência p95 (ms) | 8.12 | 28.36 | 165.87 | 419.73 |
| Latência máxima (ms) | 20 | 40 | 550 | 2484 |
| Total requisições | 276546 | 237909 | 123450 | 90846 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (GORM) (13425 req/s) | Spring WebFlux (6507 req/s) | Spring MVC (2580 req/s) | FastAPI Async (SQLAlchemy) (1529 req/s) |
| Ramp-up | Go + Gin (GORM) (12856 req/s) | Spring WebFlux (9641 req/s) | Spring MVC (3046 req/s) | FastAPI Async (SQLAlchemy) (1584 req/s) |
| Spike | Go + Gin (GORM) (3684 req/s) | Spring WebFlux (3171 req/s) | Spring MVC (1644 req/s) | FastAPI Async (SQLAlchemy) (1211 req/s) |

## Observações

- **Go + Gin (GORM)** teve o maior throughput geral em 12cpus-12gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin (GORM)** (13425 req/s), menor p95 = **Go + Gin (GORM)** (16.88 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin (GORM)** (12856 req/s), menor p95 = **Go + Gin (GORM)** (36.98 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin (GORM)** (3684 req/s), menor p95 = **Go + Gin (GORM)** (8.12 ms)
