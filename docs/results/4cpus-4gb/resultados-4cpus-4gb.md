# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, demais stacks atualizadas para 30). FastAPI com 4 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 16476.1 | 10302 | 14176.0 | 3040 | 1162 | 2319.2 |
| Latência média (ms) | 12.05 | 19 | 14.01 | 65.61 | 171.65 | 85.89 |
| Latência p50 (ms) | 11.97 | 17 | 13.21 | 59.46 | 73.81 | 4.91 |
| Latência p90 (ms) | 13.18 | 33 | 22.88 | 138.55 | 398.56 | 246.88 |
| Latência p95 (ms) | 13.68 | 41 | 28.54 | 187.05 | 583.51 | 302.00 |
| Latência máxima (ms) | 533 | 598 | 139 | 1683 | 6830 | 1084 |
| Total requisições | 494661 | 309426 | 425712 | 91515 | 35034 | 69969 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15721.7 | 10805 | 13324.9 | 4919 | 5729 | 2272.4 |
| Latência média (ms) | 13.62 | 20 | 16.08 | 43.79 | 37.53 | 95.34 |
| Latência p50 (ms) | 12.13 | 16 | 12.58 | 27.82 | 28.23 | 4.72 |
| Latência p90 (ms) | 27.83 | 43 | 34.23 | 121.80 | 85.52 | 286.51 |
| Latência p95 (ms) | 30.07 | 53 | 38.84 | 133.40 | 107.07 | 417.66 |
| Latência máxima (ms) | 65 | 191 | 304 | 166 | 461 | 2576 |
| Total requisições | 1257753 | 864432 | 1066008 | 393513 | 458373 | 181800 |
| Erros | 0,00% | 0.23% | 0,00% | 0,00% | 0,06% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3836.2 | 3217 | 3651.1 | 2186 | 2654 | 1448.3 |
| Latência média (ms) | 1.8 | 9 | 3.59 | 28.49 | 17.47 | 60.80 |
| Latência p50 (ms) | 1.23 | 4 | 1.77 | 1.58 | 4.20 | 2.77 |
| Latência p90 (ms) | 4.04 | 21 | 9.04 | 97.61 | 51.71 | 262.88 |
| Latência p95 (ms) | 5.17 | 27 | 11.82 | 104.07 | 81.60 | 306.93 |
| Latência máxima (ms) | 16 | 294 | 66 | 138 | 373 | 1687 |
| Total requisições | 287937 | 241554 | 274011 | 164127 | 199287 | 108663 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16476.1 req/s) | Go + Gin (GORM) (14176.0 req/s) | Node Fastify (10302 req/s) | Spring WebFlux (3040 req/s) | FastAPI Async (SQLAlchemy) (2319.2 req/s) | Spring MVC (1162 req/s) |
| Ramp-up | Rust + Axum (sqlx) (16476.1 req/s) | Node Fastify (10805 req/s) | Go + Gin (GORM) (14176.0 req/s) | Spring MVC (5729 req/s) | Spring WebFlux (4919 req/s) | FastAPI Async (SQLAlchemy) (2272.4 req/s) |
| Spike | Rust + Axum (sqlx) (16476.1 req/s) | Go + Gin (GORM) (14176.0 req/s) | Node Fastify (3217 req/s) | Spring MVC (2655 req/s) | Spring WebFlux (2186 req/s) | FastAPI Async (SQLAlchemy) (1448.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 4cpus-4gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em Ramp-up (10805 req/s, superando Go) e terceiro em Steady State (10302 req/s) e Spike (3217 req/s).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (14906 req/s), menor p95 = **Rust + Axum (sqlx)** (15.40 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14421 req/s), menor p95 = **Rust + Axum (sqlx)** (33.08 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3759 req/s), menor p95 = **Rust + Axum (sqlx)** (7.79 ms)
