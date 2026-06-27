# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). FastAPI com 12 workers. Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.396 | 13.822 | 13.501 | 8.020 | 6.284 | 5.237 |
| Latência média (ms) | 12,10 | 14,36 | 14,71 | 24,82 | 31,67 | 37,90 |
| Latência p50 (ms) | 11,89 | 13,75 | 14,39 | 25,52 | 6,72 | 6,13 |
| Latência p90 (ms) | 13,16 | 16,35 | 16,02 | 53,86 | 77,72 | 102,07 |
| Latência p95 (ms) | 13,93 | 17,61 | 16,89 | 64,30 | 109,76 | 182,59 |
| Latência máxima (ms) | 527 | 571 | 643 | 933 | 2153 | 1992 |
| Total requisições | 492.249 | 415.038 | 405.528 | 240.897 | 188.907 | 158.169 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 15.922 | 14.162 | 13.154 | 11.027 | 8.061 | 4.949 |
| Latência média (ms) | 13,44 | 15,12 | 16,29 | 19,44 | 26,64 | 43,57 |
| Latência p50 (ms) | 11,77 | 13,38 | 14,41 | 12,53 | 17,34 | 5,91 |
| Latência p90 (ms) | 27,20 | 30,59 | 33,15 | 51,89 | 66,84 | 139,14 |
| Latência p95 (ms) | 29,94 | 33,07 | 35,92 | 57,91 | 87,50 | 186,31 |
| Latência máxima (ms) | 68 | 81 | 76 | 97 | 420 | 1621 |
| Total requisições | 1.273.806 | 1.132.962 | 1.052.322 | 882.150 | 644.871 | 395.925 |
| Erros | 0,00% | 0,00% | 0,00% | 0,23% | 0,13% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.844 | 3.774 | 3.734 | 3.387 | 2.850 | 2.092 |
| Latência média (ms) | 1,74 | 2,37 | 2,76 | 6,47 | 13,96 | 31,38 |
| Latência p50 (ms) | 1,24 | 1,61 | 1,69 | 1,90 | 3,14 | 2,88 |
| Latência p90 (ms) | 3,89 | 5,12 | 6,38 | 18,19 | 39,93 | 105,80 |
| Latência p95 (ms) | 5,13 | 6,57 | 7,70 | 20,31 | 69,11 | 166,42 |
| Latência máxima (ms) | 14 | 25 | 37 | 36 | 431 | 1719 |
| Total requisições | 288.351 | 283.263 | 280.290 | 254.130 | 213.990 | 157.128 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.396 req/s) | Node Fastify (13.822 req/s) | Go + Gin (GORM) (13.501 req/s) | Spring WebFlux (8.020 req/s) | Spring MVC (6.284 req/s) | FastAPI Async (SQLAlchemy) (5.237 req/s) |
| Ramp-up | Rust + Axum (sqlx) (15.922 req/s) | Node Fastify (14.162 req/s) | Go + Gin (GORM) (13.154 req/s) | Spring WebFlux (11.027 req/s) | Spring MVC (8.061 req/s) | FastAPI Async (SQLAlchemy) (4.949 req/s) |
| Spike | Rust + Axum (sqlx) (3.844 req/s) | Node Fastify (3.774 req/s) | Go + Gin (GORM) (3.734 req/s) | Spring WebFlux (3.387 req/s) | Spring MVC (2.850 req/s) | FastAPI Async (SQLAlchemy) (2.092 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.396 req/s), menor p95 = **Rust + Axum (sqlx)** (13,93 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (15.922 req/s), menor p95 = **Rust + Axum (sqlx)** (29,94 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.844 req/s), menor p95 = **Rust + Axum (sqlx)** (5,13 ms)
