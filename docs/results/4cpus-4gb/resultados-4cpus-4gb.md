# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=2 + max_overflow=0). FastAPI com 4 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14906 | 10302 | 12926 | 3040 | 1162 | 2319.2 |
| Latência média (ms) | 13.32 | 19 | 15.37 | 65.61 | 171.65 | 85.89 |
| Latência p50 (ms) | 13.13 | 17 | 13.56 | 59.46 | 73.81 | 4.91 |
| Latência p90 (ms) | 14.61 | 33 | 28.01 | 138.55 | 398.56 | 246.88 |
| Latência p95 (ms) | 15.40 | 41 | 35.99 | 187.05 | 583.51 | 302.00 |
| Latência máxima (ms) | 582 | 598 | 135 | 1683 | 6830 | 1084 |
| Total requisições | 447564 | 309426 | 388176 | 91515 | 35034 | 69969 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14421 | 10805 | 10118 | 4919 | 5729 | 2272.4 |
| Latência média (ms) | 14.85 | 20 | 21.30 | 43.79 | 37.53 | 95.34 |
| Latência p50 (ms) | 12.82 | 16 | 11.17 | 27.82 | 28.23 | 4.72 |
| Latência p90 (ms) | 30.47 | 43 | 34.84 | 121.80 | 85.52 | 286.51 |
| Latência p95 (ms) | 33.08 | 53 | 49.57 | 133.40 | 107.07 | 417.66 |
| Latência máxima (ms) | 74 | 191 | 1165 | 166 | 461 | 2576 |
| Total requisições | 1153725 | 864432 | 809442 | 393513 | 458373 | 181800 |
| Erros | 0,00% | 0.23% | 0,00% | 0,00% | 0,06% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3759 | 3217 | 3331 | 2186 | 2654 | 1448.3 |
| Latência média (ms) | 2.51 | 9 | 7.16 | 28.49 | 17.47 | 60.80 |
| Latência p50 (ms) | 1.49 | 4 | 2.96 | 1.58 | 4.20 | 2.77 |
| Latência p90 (ms) | 6.07 | 21 | 18.87 | 97.61 | 51.71 | 262.88 |
| Latência p95 (ms) | 7.79 | 27 | 24.67 | 104.07 | 81.60 | 306.93 |
| Latência máxima (ms) | 19 | 294 | 97 | 138 | 373 | 1687 |
| Total requisições | 282231 | 241554 | 249924 | 164127 | 199287 | 108663 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (14906 req/s) | Go + Gin (GORM) (12926 req/s) | Node Fastify (10302 req/s) | Spring WebFlux (3040 req/s) | FastAPI Async (SQLAlchemy) (2319.2 req/s) | Spring MVC (1162 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14421 req/s) | Node Fastify (10805 req/s) | Go + Gin (GORM) (10118 req/s) | Spring MVC (5729 req/s) | Spring WebFlux (4919 req/s) | FastAPI Async (SQLAlchemy) (2272.4 req/s) |
| Spike | Rust + Axum (sqlx) (3759 req/s) | Go + Gin (GORM) (3331 req/s) | Node Fastify (3217 req/s) | Spring MVC (2655 req/s) | Spring WebFlux (2186 req/s) | FastAPI Async (SQLAlchemy) (1448.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 4cpus-4gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em Ramp-up (10805 req/s, superando Go) e terceiro em Steady State (10302 req/s) e Spike (3217 req/s).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (14906 req/s), menor p95 = **Rust + Axum (sqlx)** (15.40 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14421 req/s), menor p95 = **Rust + Axum (sqlx)** (33.08 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3759 req/s), menor p95 = **Rust + Axum (sqlx)** (7.79 ms)
