# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). FastAPI com 8 workers. Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.645 | 13.808 | 13.296 | 6.112 | 4.412 | 4.021 |
| Latência média (ms) | 11,92 | 14,38 | 14,94 | 32,60 | 45,15 | 49,50 |
| Latência p50 (ms) | 11,71 | 13,61 | 14,57 | 32,77 | 7,57 | 5,53 |
| Latência p90 (ms) | 12,95 | 16,42 | 16,60 | 74,61 | 111,91 | 135,93 |
| Latência p95 (ms) | 13,74 | 18,35 | 17,52 | 87,19 | 158,03 | 192,65 |
| Latência máxima (ms) | 529 | 521 | 626 | 1218 | 3536 | 1007 |
| Total requisições | 499.728 | 414.609 | 399.345 | 183.621 | 132.612 | 121.158 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.094 | 14.257 | 13.251 | 8.638 | 7.889 | 3.816 |
| Latência média (ms) | 13,30 | 15,02 | 16,17 | 24,87 | 27,22 | 56,67 |
| Latência p50 (ms) | 11,66 | 13,18 | 14,52 | 15,81 | 17,87 | 5,19 |
| Latência p90 (ms) | 27,15 | 30,55 | 32,69 | 67,81 | 67,66 | 179,95 |
| Latência p95 (ms) | 29,60 | 33,09 | 35,48 | 76,46 | 88,93 | 264,25 |
| Latência máxima (ms) | 59 | 81 | 80 | 99 | 385 | 1953 |
| Total requisições | 1.287.516 | 1.140.573 | 1.060.089 | 691.020 | 631.143 | 305.247 |
| Erros | 0,00% | 0,00% | 0,00% | 0,03% | 0,03% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.848 | 3.744 | 3.745 | 2.993 | 2.838 | 1.855 |
| Latência média (ms) | 1,69 | 2,67 | 2,64 | 11,72 | 14,15 | 39,75 |
| Latência p50 (ms) | 1,21 | 1,59 | 1,59 | 1,81 | 3,28 | 2,79 |
| Latência p90 (ms) | 3,72 | 6,53 | 6,35 | 35,02 | 40,37 | 146,54 |
| Latência p95 (ms) | 4,78 | 8,22 | 7,91 | 37,70 | 69,92 | 209,65 |
| Latência máxima (ms) | 18 | 25 | 31 | 55 | 438 | 1766 |
| Total requisições | 288.801 | 281.001 | 281.238 | 224.730 | 213.099 | 139.179 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.645 req/s) | Node Fastify (13.808 req/s) | Go + Gin (GORM) (13.296 req/s) | Spring WebFlux (6.112 req/s) | Spring MVC (4.412 req/s) | FastAPI Async (SQLAlchemy) (4.021 req/s) |
| Ramp-up | Rust + Axum (sqlx) (16.094 req/s) | Node Fastify (14.257 req/s) | Go + Gin (GORM) (13.251 req/s) | Spring WebFlux (8.638 req/s) | Spring MVC (7.889 req/s) | FastAPI Async (SQLAlchemy) (3.816 req/s) |
| Spike | Rust + Axum (sqlx) (3.848 req/s) | Go + Gin (GORM) (3.745 req/s) | Node Fastify (3.744 req/s) | Spring WebFlux (2.993 req/s) | Spring MVC (2.838 req/s) | FastAPI Async (SQLAlchemy) (1.855 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.645 req/s), menor p95 = **Rust + Axum (sqlx)** (13,74 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (16.094 req/s), menor p95 = **Rust + Axum (sqlx)** (29,60 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.848 req/s), menor p95 = **Rust + Axum (sqlx)** (4,78 ms)
