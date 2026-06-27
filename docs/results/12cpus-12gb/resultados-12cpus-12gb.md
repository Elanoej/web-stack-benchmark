# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.396 | 13.822 | 13.501 | 7.559 | 6.000 | 5.237 |
| Latência média (ms) | 12,10 | 14,36 | 14,71 | 26,33 | 33,18 | 37,90 |
| Latência p50 (ms) | 11,89 | 13,75 | 14,39 | 26,91 | 9,97 | 6,13 |
| Latência p90 (ms) | 13,16 | 16,35 | 16,02 | 58,61 | 84,23 | 102,07 |
| Latência p95 (ms) | 13,93 | 17,61 | 16,89 | 69,22 | 114,38 | 182,59 |
| Latência máxima (ms) | 527,07 | 570,63 | 643,10 | 685,10 | 2.298,55 | 1.991,83 |
| Total requisições | 492.249 | 415.038 | 405.528 | 227.070 | 180.321 | 158.169 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 15.922 | 14.162 | 13.154 | 10.468 | 8.547 | 4.949 |
| Latência média (ms) | 13,44 | 15,12 | 16,29 | 20,48 | 25,10 | 43,57 |
| Latência p50 (ms) | 11,77 | 13,38 | 14,41 | 14,18 | 13,83 | 5,91 |
| Latência p90 (ms) | 27,20 | 30,59 | 33,15 | 51,70 | 63,57 | 139,14 |
| Latência p95 (ms) | 29,94 | 33,07 | 35,92 | 60,71 | 89,97 | 186,31 |
| Latência máxima (ms) | 67,64 | 81,14 | 75,72 | 107,28 | 711,78 | 1.620,61 |
| Total requisições | 1.273.806 | 1.132.962 | 1.052.322 | 837.480 | 683.784 | 395.925 |
| Erros | **0,00%** | **0,00%** | **0,00%** | 0,26% | 0,66% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.844 | 3.774 | 3.734 | 3.327 | 2.937 | 2.092 |
| Latência média (ms) | 1,74 | 2,37 | 2,76 | 7,19 | 12,57 | 31,38 |
| Latência p50 (ms) | 1,24 | 1,61 | 1,69 | 1,91 | 3,28 | 2,88 |
| Latência p90 (ms) | 3,89 | 5,12 | 6,38 | 20,17 | 36,10 | 105,80 |
| Latência p95 (ms) | 5,13 | 6,57 | 7,70 | 21,72 | 60,46 | 166,42 |
| Latência máxima (ms) | 14,32 | 25,18 | 37,01 | 36,38 | 306,96 | 1.719,15 |
| Total requisições | 288.351 | 283.263 | 280.290 | 249.687 | 220.284 | 157.128 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.396 req/s) | Node Fastify (13.822 req/s) | Go + Gin (GORM) (13.501 req/s) | Spring WebFlux (7.559 req/s) | Spring MVC (6.000 req/s) | FastAPI Async (SQLAlchemy) (5.237 req/s) |
| Ramp-up | Rust + Axum (sqlx) (15.922 req/s) | Node Fastify (14.162 req/s) | Go + Gin (GORM) (13.154 req/s) | Spring WebFlux (10.468 req/s) | Spring MVC (8.547 req/s) | FastAPI Async (SQLAlchemy) (4.949 req/s) |
| Spike | Rust + Axum (sqlx) (3.844 req/s) | Node Fastify (3.774 req/s) | Go + Gin (GORM) (3.734 req/s) | Spring WebFlux (3.327 req/s) | Spring MVC (2.937 req/s) | FastAPI Async (SQLAlchemy) (2.092 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.396 req/s), menor p95 = **Rust + Axum (sqlx)** (13,93 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (15.922 req/s), menor p95 = **Rust + Axum (sqlx)** (29,94 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.844 req/s), menor p95 = **Rust + Axum (sqlx)** (5,13 ms)