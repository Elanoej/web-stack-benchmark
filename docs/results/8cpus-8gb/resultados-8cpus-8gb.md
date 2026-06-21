# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. FastAPI com 9 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 11281 | 14632 | 4235 | 2464 | 2287 |
| Latência média (ms) | 17.61 | 13.57 | 47.07 | 80.79 | 86.85 |
| Latência p50 (ms) | 16.86 | 13.25 | 40.13 | 90.23 | 19.28 |
| Latência p90 (ms) | 19.74 | 14.82 | 92.96 | 191.14 | 254.68 |
| Latência p95 (ms) | 22.66 | 15.83 | 103.94 | 218.70 | 324.15 |
| Latência máxima (ms) | 507 | 589 | 1141 | 1571 | 2001 |
| Total requisições | 338850 | 439308 | 127269 | 74358 | 69420 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 43.37% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 10921 | 14319 | 7629 | 3062 | 1626 |
| Latência média (ms) | 19.63 | 14.96 | 28.17 | 70.46 | 133.36 |
| Latência p50 (ms) | 17.16 | 12.91 | 18.02 | 55.46 | 66.54 |
| Latência p90 (ms) | 40.53 | 30.71 | 78.25 | 166.06 | 350.43 |
| Latência p95 (ms) | 44.44 | 33.43 | 87.67 | 189.63 | 454.96 |
| Latência máxima (ms) | 97 | 76 | 134 | 650 | 2626 |
| Total requisições | 873681 | 1145559 | 610350 | 244989 | 130056 |
| Erros | 0,00% | 0,00% | 0.12% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 3390 | 3761 | 2792 | 1643 | 1237 |
| Latência média (ms) | 6.41 | 2.48 | 15.02 | 49.10 | 76.85 |
| Latência p50 (ms) | 5.38 | 1.50 | 1.88 | 10.69 | 5.98 |
| Latência p90 (ms) | 14.16 | 5.67 | 46.02 | 156.69 | 363.17 |
| Latência p95 (ms) | 15.93 | 7.20 | 49.11 | 167.95 | 409.51 |
| Latência máxima (ms) | 49 | 28 | 81 | 518 | 2979 |
| Total requisições | 254529 | 282402 | 209427 | 123393 | 92904 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (14632 req/s) | Go + Gin (GORM) (11281 req/s) | Spring WebFlux (4235 req/s) | Spring MVC (2464 req/s) | FastAPI Async (SQLAlchemy) (2287 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14319 req/s) | Go + Gin (GORM) (10921 req/s) | Spring WebFlux (7629 req/s) | Spring MVC (3062 req/s) | FastAPI Async (SQLAlchemy) (1626 req/s) |
| Spike | Rust + Axum (sqlx) (3761 req/s) | Go + Gin (GORM) (3390 req/s) | Spring WebFlux (2792 req/s) | Spring MVC (1643 req/s) | FastAPI Async (SQLAlchemy) (1237 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (14632 req/s), menor p95 = **Rust + Axum (sqlx)** (15.83 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14319 req/s), menor p95 = **Rust + Axum (sqlx)** (33.43 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3761 req/s), menor p95 = **Rust + Axum (sqlx)** (7.20 ms)
