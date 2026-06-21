# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 5 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 12926 | 14906 | 1932 | 1421 | 2478 |
| Latência média (ms) | 15.37 | 13.32 | 103.29 | 140.14 | 79.88 |
| Latência p50 (ms) | 13.56 | 13.13 | 103.18 | 114.01 | 18.02 |
| Latência p90 (ms) | 28.01 | 14.61 | 183.86 | 309.13 | 181.43 |
| Latência p95 (ms) | 35.99 | 15.40 | 226.25 | 432.23 | 451.03 |
| Latência máxima (ms) | 135 | 582 | 1618 | 3118 | 2457 |
| Total requisições | 388176 | 447564 | 58137 | 42912 | 75711 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 53.36% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 10118 | 14421 | 4746 | 3047 | 1606 |
| Latência média (ms) | 21.30 | 14.85 | 45.39 | 70.80 | 135.03 |
| Latência p50 (ms) | 11.17 | 12.82 | 29.05 | 56.53 | 67.53 |
| Latência p90 (ms) | 34.84 | 30.47 | 126.36 | 166.38 | 364.04 |
| Latência p95 (ms) | 49.57 | 33.08 | 141.47 | 187.01 | 462.70 |
| Latência máxima (ms) | 1165 | 74 | 171 | 525 | 3203 |
| Total requisições | 809442 | 1153725 | 379689 | 243798 | 128517 |
| Erros | 0,00% | 0,00% | 0.01% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 3331 | 3759 | 2137 | 1644 | 1224 |
| Latência média (ms) | 7.16 | 2.51 | 29.94 | 49.14 | 77.98 |
| Latência p50 (ms) | 2.96 | 1.49 | 1.69 | 10.84 | 6.27 |
| Latência p90 (ms) | 18.87 | 6.07 | 105.59 | 156.69 | 371.24 |
| Latência p95 (ms) | 24.67 | 7.79 | 110.80 | 167.69 | 414.06 |
| Latência máxima (ms) | 97 | 19 | 134 | 579 | 2580 |
| Total requisições | 249924 | 282231 | 160338 | 123300 | 91956 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (14906 req/s) | Go + Gin (GORM) (12926 req/s) | FastAPI Async (SQLAlchemy) (2478 req/s) | Spring WebFlux (1932 req/s) | Spring MVC (1421 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14421 req/s) | Go + Gin (GORM) (10118 req/s) | Spring WebFlux (4746 req/s) | Spring MVC (3047 req/s) | FastAPI Async (SQLAlchemy) (1606 req/s) |
| Spike | Rust + Axum (sqlx) (3759 req/s) | Go + Gin (GORM) (3331 req/s) | Spring WebFlux (2137 req/s) | Spring MVC (1644 req/s) | FastAPI Async (SQLAlchemy) (1224 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 4cpus-4gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (14906 req/s), menor p95 = **Rust + Axum (sqlx)** (15.40 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14421 req/s), menor p95 = **Rust + Axum (sqlx)** (33.08 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3759 req/s), menor p95 = **Rust + Axum (sqlx)** (7.79 ms)
