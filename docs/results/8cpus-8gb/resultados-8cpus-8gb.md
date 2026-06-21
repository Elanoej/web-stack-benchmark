# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 9 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 11281 | 15332 | 4235 | 2464 | 2287 |
| Latência média (ms) | 17.61 | 12.95 | 47.07 | 80.79 | 86.85 |
| Latência p50 (ms) | 16.86 | 12.70 | 40.13 | 90.23 | 19.28 |
| Latência p90 (ms) | 19.74 | 14.05 | 92.96 | 191.14 | 254.68 |
| Latência p95 (ms) | 22.66 | 14.97 | 103.94 | 218.70 | 324.15 |
| Latência máxima (ms) | 507 | 460 | 1141 | 1571 | 2001 |
| Total requisições | 338850 | 460356 | 127269 | 74358 | 69420 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 43.37% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 10921 | 14762 | 7629 | 3062 | 1626 |
| Latência média (ms) | 19.63 | 14.51 | 28.17 | 70.46 | 133.36 |
| Latência p50 (ms) | 17.16 | 12.63 | 18.02 | 55.46 | 66.54 |
| Latência p90 (ms) | 40.53 | 29.79 | 78.25 | 166.06 | 350.43 |
| Latência p95 (ms) | 44.44 | 32.21 | 87.67 | 189.63 | 454.96 |
| Latência máxima (ms) | 97 | 73 | 134 | 650 | 2626 |
| Total requisições | 873681 | 1180959 | 610350 | 244989 | 130056 |
| Erros | 0,00% | 0,00% | 0.12% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 3390 | 3778 | 2792 | 1643 | 1237 |
| Latência média (ms) | 6.41 | 2.31 | 15.02 | 49.10 | 76.85 |
| Latência p50 (ms) | 5.38 | 1.47 | 1.88 | 10.69 | 5.98 |
| Latência p90 (ms) | 14.16 | 5.33 | 46.02 | 156.69 | 363.17 |
| Latência p95 (ms) | 15.93 | 6.56 | 49.11 | 167.95 | 409.51 |
| Latência máxima (ms) | 49 | 20 | 81 | 518 | 2979 |
| Total requisições | 254529 | 283722 | 209427 | 123393 | 92904 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (15332 req/s) | Go + Gin (GORM) (11281 req/s) | Spring WebFlux (4235 req/s) | Spring MVC (2464 req/s) | FastAPI Async (SQLAlchemy) (2287 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14762 req/s) | Go + Gin (GORM) (10921 req/s) | Spring WebFlux (7629 req/s) | Spring MVC (3062 req/s) | FastAPI Async (SQLAlchemy) (1626 req/s) |
| Spike | Rust + Axum (sqlx) (3778 req/s) | Go + Gin (GORM) (3390 req/s) | Spring WebFlux (2792 req/s) | Spring MVC (1643 req/s) | FastAPI Async (SQLAlchemy) (1237 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15332 req/s), menor p95 = **Rust + Axum (sqlx)** (14.97 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14762 req/s), menor p95 = **Rust + Axum (sqlx)** (32.21 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3778 req/s), menor p95 = **Rust + Axum (sqlx)** (6.56 ms)
