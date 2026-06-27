# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 13.397 | 6.219 | 8.717 | 709,7 | 245,0 | 1.198 |
| Latência média (ms) | 14,84 | 32,04 | 22,84 | 280,72 | 806,51 | 166,17 |
| Latência p50 (ms) | 20,46 | 28,81 | 15,20 | 284,61 | 203,07 | 236,23 |
| Latência p90 (ms) | 23,34 | 52,46 | 55,41 | 506,74 | 1.808,00 | 479,32 |
| Latência p95 (ms) | 24,07 | 61,78 | 73,12 | 800,37 | 2.897,98 | 499,75 |
| Latência máxima (ms) | 51,17 | 1.429,40 | 398,64 | 2.186,54 | 10.695,10 | 1.765,61 |
| Total requisições | 402.303 | 187.032 | 261.993 | 21.507 | 7.557 | 36.273 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 13.375 | 5.993 | 8.668 | 2.396 | 994,2 | 1.189 |
| Latência média (ms) | 16,03 | 35,93 | 24,81 | 90,14 | 219,36 | 183,31 |
| Latência p50 (ms) | 9,47 | 28,64 | 9,51 | 91,90 | 105,40 | 6,62 |
| Latência p90 (ms) | 43,70 | 74,74 | 67,25 | 210,60 | 590,82 | 558,67 |
| Latência p95 (ms) | 49,68 | 88,85 | 102,15 | 250,03 | 799,60 | 693,05 |
| Latência máxima (ms) | 78,00 | 1.701,55 | 802,98 | 379,38 | 3.189,92 | 4.490,93 |
| Total requisições | 1.070.019 | 479.484 | 693.453 | 191.685 | 79.542 | 95.133 |
| Erros | 0,29% | 0,01% | 0,08% | 0,00% | **0,00%** | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.771 | 2.310 | 2.941 | 1.671 | 1.771 | 1.051 |
| Latência média (ms) | 2,44 | 25,24 | 12,55 | 47,83 | 43,20 | 97,35 |
| Latência p50 (ms) | 1,29 | 7,53 | 2,14 | 1,46 | 3,42 | 4,40 |
| Latência p90 (ms) | 6,52 | 47,30 | 38,60 | 196,04 | 109,81 | 515,05 |
| Latência p95 (ms) | 8,08 | 57,94 | 56,95 | 214,67 | 203,00 | 600,64 |
| Latência máxima (ms) | 29,43 | 1.472,97 | 328,93 | 357,38 | 1.114,56 | 3.018,73 |
| Total requisições | 282.903 | 173.307 | 220.737 | 125.409 | 132.837 | 78.855 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (13.397 req/s) | Go + Gin (GORM) (8.717 req/s) | Node Fastify (6.219 req/s) | FastAPI Async (SQLAlchemy) (1.198 req/s) | Spring WebFlux (710 req/s) | Spring MVC (245 req/s) |
| Ramp-up | Rust + Axum (sqlx) (13.375 req/s) | Go + Gin (GORM) (8.668 req/s) | Node Fastify (5.993 req/s) | Spring WebFlux (2.396 req/s) | FastAPI Async (SQLAlchemy) (1.189 req/s) | Spring MVC (994 req/s) |
| Spike | Rust + Axum (sqlx) (3.771 req/s) | Go + Gin (GORM) (2.941 req/s) | Node Fastify (2.310 req/s) | Spring MVC (1.771 req/s) | Spring WebFlux (1.671 req/s) | FastAPI Async (SQLAlchemy) (1.051 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-2gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (13.397 req/s), menor p95 = **Rust + Axum (sqlx)** (24,07 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (13.375 req/s), menor p95 = **Rust + Axum (sqlx)** (49,68 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.771 req/s), menor p95 = **Rust + Axum (sqlx)** (8,08 ms)