# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). FastAPI com 1 workers. Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.657 | 3.096 | 4.249 | 174,7 | 143,5 | 604,2 |
| Latência média (ms) | 26,02 | 64,36 | 46,86 | 1.134,42 | 1.365,90 | 328,32 |
| Latência p50 (ms) | 35,74 | 50,40 | 21,31 | 1.000,45 | 400,89 | 488,96 |
| Latência p90 (ms) | 41,70 | 89,47 | 107,37 | 2.588,86 | 4.196,21 | 501,33 |
| Latência p95 (ms) | 44,01 | 102,66 | 164,69 | 3.206,81 | 5.300,22 | 531,48 |
| Latência máxima (ms) | 58 | 4605 | 506 | 6587 | 13695 | 1516 |
| Total requisições | 230.082 | 93.351 | 127.887 | 5.400 | 4.527 | 18.468 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.709 | 3.144 | 4.247 | 579,3 | 400,1 | 592,7 |
| Latência média (ms) | 27,90 | 71,28 | 50,80 | 378,09 | 553,97 | 371,28 |
| Latência p50 (ms) | 15,82 | 41,31 | 12,11 | 295,18 | 392,84 | 145,56 |
| Latência p90 (ms) | 77,91 | 79,32 | 127,60 | 983,79 | 1.302,36 | 1.087,87 |
| Latência p95 (ms) | 88,72 | 92,61 | 204,75 | 1.087,00 | 1.795,53 | 1.234,78 |
| Latência máxima (ms) | 120 | 9098 | 2598 | 1402 | 6006 | 6241 |
| Total requisições | 616.764 | 251.544 | 339.729 | 46.347 | 32.013 | 47.415 |
| Erros | 0,01% | 0,00% | 0,03% | 0,00% | 0,00% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.764 | 1.685 | 1.983 | 1.130 | 661,0 | 578,3 |
| Latência média (ms) | 15,51 | 48,55 | 34,89 | 87,84 | 177,45 | 209,32 |
| Latência p50 (ms) | 1,91 | 1,62 | 1,36 | 1,92 | 85,93 | 6,96 |
| Latência p90 (ms) | 47,97 | 60,16 | 108,15 | 511,07 | 501,59 | 1.022,16 |
| Latência p95 (ms) | 52,42 | 76,05 | 193,39 | 600,88 | 892,89 | 1.220,68 |
| Latência máxima (ms) | 72 | 7106 | 1286 | 799 | 3905 | 8541 |
| Total requisições | 207.471 | 126.465 | 148.899 | 84.873 | 49.590 | 43.401 |
| Erros | 0,00% | 0,00% | 0,00% | 0,01% | 0,76% | 0,04% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.657 req/s) | Go + Gin (GORM) (4.249 req/s) | Node Fastify (3.096 req/s) | FastAPI Async (SQLAlchemy) (604,2 req/s) | Spring WebFlux (174,7 req/s) | Spring MVC (143,5 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.709 req/s) | Go + Gin (GORM) (4.247 req/s) | Node Fastify (3.144 req/s) | FastAPI Async (SQLAlchemy) (592,7 req/s) | Spring WebFlux (579,3 req/s) | Spring MVC (400,1 req/s) |
| Spike | Rust + Axum (sqlx) (2.764 req/s) | Go + Gin (GORM) (1.983 req/s) | Node Fastify (1.685 req/s) | Spring WebFlux (1.130 req/s) | Spring MVC (661,0 req/s) | FastAPI Async (SQLAlchemy) (578,3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (7.657 req/s), menor p95 = **Rust + Axum (sqlx)** (44,01 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7.709 req/s), menor p95 = **Rust + Axum (sqlx)** (88,72 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2.764 req/s), menor p95 = **Rust + Axum (sqlx)** (52,42 ms)
