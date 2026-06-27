# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.645 | 13.808 | 13.296 | 6.139 | 4.136 | 4.021 |
| Latência média (ms) | 11,92 | 14,38 | 14,94 | 32,46 | 48,18 | 49,50 |
| Latência p50 (ms) | 11,71 | 13,61 | 14,57 | 32,29 | 13,01 | 5,53 |
| Latência p90 (ms) | 12,95 | 16,42 | 16,60 | 75,47 | 117,41 | 135,93 |
| Latência p95 (ms) | 13,74 | 18,35 | 17,52 | 89,01 | 170,46 | 192,65 |
| Latência máxima (ms) | 529,20 | 520,65 | 625,84 | 869,70 | 3.065,52 | 1.006,96 |
| Total requisições | 499.728 | 414.609 | 399.345 | 184.455 | 124.299 | 121.158 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.094 | 14.257 | 13.251 | 8.771 | 8.538 | 3.816 |
| Latência média (ms) | 13,30 | 15,02 | 16,17 | 24,49 | 25,13 | 56,67 |
| Latência p50 (ms) | 11,66 | 13,18 | 14,52 | 15,43 | 13,91 | 5,19 |
| Latência p90 (ms) | 27,15 | 30,55 | 32,69 | 67,18 | 63,75 | 179,95 |
| Latência p95 (ms) | 29,60 | 33,09 | 35,48 | 75,25 | 89,46 | 264,25 |
| Latência máxima (ms) | 59,29 | 80,52 | 80,05 | 126,72 | 489,34 | 1.953,04 |
| Total requisições | 1.287.516 | 1.140.573 | 1.060.089 | 701.691 | 683.085 | 305.247 |
| Erros | **0,00%** | **0,00%** | **0,00%** | 0,39% | 0,76% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.848 | 3.744 | 3.745 | 3.018 | 2.940 | 1.855 |
| Latência média (ms) | 1,69 | 2,67 | 2,64 | 11,38 | 12,47 | 39,75 |
| Latência p50 (ms) | 1,21 | 1,59 | 1,59 | 1,69 | 3,20 | 2,79 |
| Latência p90 (ms) | 3,72 | 6,53 | 6,35 | 33,91 | 35,95 | 146,54 |
| Latência p95 (ms) | 4,78 | 8,22 | 7,91 | 36,28 | 60,13 | 209,65 |
| Latência máxima (ms) | 17,55 | 25,01 | 31,49 | 47,89 | 301,90 | 1.765,93 |
| Total requisições | 288.801 | 281.001 | 281.238 | 226.410 | 220.749 | 139.179 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.645 req/s) | Node Fastify (13.808 req/s) | Go + Gin (GORM) (13.296 req/s) | Spring WebFlux (6.139 req/s) | Spring MVC (4.136 req/s) | FastAPI Async (SQLAlchemy) (4.021 req/s) |
| Ramp-up | Rust + Axum (sqlx) (16.094 req/s) | Node Fastify (14.257 req/s) | Go + Gin (GORM) (13.251 req/s) | Spring WebFlux (8.771 req/s) | Spring MVC (8.538 req/s) | FastAPI Async (SQLAlchemy) (3.816 req/s) |
| Spike | Rust + Axum (sqlx) (3.848 req/s) | Go + Gin (GORM) (3.745 req/s) | Node Fastify (3.744 req/s) | Spring WebFlux (3.018 req/s) | Spring MVC (2.940 req/s) | FastAPI Async (SQLAlchemy) (1.855 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.645 req/s), menor p95 = **Rust + Axum (sqlx)** (13,74 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (16.094 req/s), menor p95 = **Rust + Axum (sqlx)** (29,60 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.848 req/s), menor p95 = **Rust + Axum (sqlx)** (4,78 ms)