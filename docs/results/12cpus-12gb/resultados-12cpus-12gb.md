# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. FastAPI com 13 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 11137 | 14375 | 6507 | 2580 | 1529 |
| Latência média (ms) | 17.83 | 13.81 | 30.60 | 77.14 | 130.00 |
| Latência p50 (ms) | 17.18 | 13.52 | 29.88 | 91.27 | 99.32 |
| Latência p90 (ms) | 19.53 | 15.02 | 58.39 | 149.45 | 272.34 |
| Latência p95 (ms) | 21.48 | 15.95 | 71.46 | 218.36 | 327.46 |
| Latência máxima (ms) | 651 | 594 | 910 | 1041 | 1630 |
| Total requisições | 334527 | 431622 | 195453 | 77841 | 46308 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 10958 | 14154 | 9641 | 3046 | 1584 |
| Latência média (ms) | 19.56 | 15.13 | 22.25 | 70.84 | 137.08 |
| Latência p50 (ms) | 17.50 | 13.10 | 14.12 | 57.84 | 67.09 |
| Latência p90 (ms) | 39.85 | 31.21 | 59.17 | 165.12 | 406.67 |
| Latência p95 (ms) | 43.28 | 33.68 | 67.99 | 185.02 | 503.47 |
| Latência máxima (ms) | 98 | 68 | 109 | 524 | 3203 |
| Total requisições | 876630 | 1132350 | 771336 | 243699 | 126702 |
| Erros | 0,00% | 0,00% | 0.23% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 3379 | 3761 | 3171 | 1644 | 1211 |
| Latência média (ms) | 6.54 | 2.50 | 9.20 | 49.07 | 79.36 |
| Latência p50 (ms) | 4.77 | 1.56 | 2.24 | 10.86 | 6.23 |
| Latência p90 (ms) | 14.77 | 5.82 | 25.91 | 156.47 | 360.01 |
| Latência p95 (ms) | 16.67 | 7.07 | 28.36 | 165.87 | 419.73 |
| Latência máxima (ms) | 50 | 18 | 40 | 550 | 2484 |
| Total requisições | 253650 | 282243 | 237909 | 123450 | 90846 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (14375 req/s) | Go + Gin (GORM) (11137 req/s) | Spring WebFlux (6507 req/s) | Spring MVC (2580 req/s) | FastAPI Async (SQLAlchemy) (1529 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14154 req/s) | Go + Gin (GORM) (10958 req/s) | Spring WebFlux (9641 req/s) | Spring MVC (3046 req/s) | FastAPI Async (SQLAlchemy) (1584 req/s) |
| Spike | Rust + Axum (sqlx) (3761 req/s) | Go + Gin (GORM) (3379 req/s) | Spring WebFlux (3171 req/s) | Spring MVC (1644 req/s) | FastAPI Async (SQLAlchemy) (1211 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (14375 req/s), menor p95 = **Rust + Axum (sqlx)** (15.95 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14154 req/s), menor p95 = **Rust + Axum (sqlx)** (33.68 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3761 req/s), menor p95 = **Rust + Axum (sqlx)** (7.07 ms)
