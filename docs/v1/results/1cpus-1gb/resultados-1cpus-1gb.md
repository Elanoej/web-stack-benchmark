# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.657 | 3.096 | 4.249 | 201,9 | 59,9 | 604,2 |
| Latência média (ms) | 26,02 | 64,36 | 46,86 | 976,86 | 3.237,64 | 328,32 |
| Latência p50 (ms) | 35,74 | 50,40 | 21,31 | 903,69 | 898,01 | 488,96 |
| Latência p90 (ms) | 41,70 | 89,47 | 107,37 | 2.096,84 | 15.697,90 | 501,33 |
| Latência p95 (ms) | 44,01 | 102,66 | 164,69 | 2.675,31 | 17.100,96 | 531,48 |
| Latência máxima (ms) | 57,79 | 4.605,17 | 506,48 | 4.397,94 | 18.401,47 | 1.515,95 |
| Total requisições | 230.082 | 93.351 | 127.887 | 6.219 | 1.929 | 18.468 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.709 | 3.144 | 4.247 | 587,1 | 405,6 | 592,7 |
| Latência média (ms) | 27,90 | 71,28 | 50,80 | 372,17 | 545,68 | 371,28 |
| Latência p50 (ms) | 15,82 | 41,31 | 12,11 | 301,55 | 396,46 | 145,56 |
| Latência p90 (ms) | 77,91 | 79,32 | 127,60 | 901,88 | 1.292,68 | 1.087,87 |
| Latência p95 (ms) | 88,72 | 92,61 | 204,75 | 995,60 | 1.798,05 | 1.234,78 |
| Latência máxima (ms) | 119,92 | 9.097,87 | 2.598,36 | 1.194,36 | 6.501,63 | 6.241,30 |
| Total requisições | 616.764 | 251.544 | 339.729 | 46.977 | 32.448 | 47.415 |
| Erros | 0,01% | **0,00%** | 0,03% | **0,00%** | **0,00%** | **0,00%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.764 | 1.685 | 1.983 | 1.085 | 684,1 | 578,3 |
| Latência média (ms) | 15,51 | 48,55 | 34,89 | 92,70 | 170,64 | 209,32 |
| Latência p50 (ms) | 1,91 | 1,62 | 1,36 | 2,10 | 8,03 | 6,96 |
| Latência p90 (ms) | 47,97 | 60,16 | 108,15 | 516,60 | 493,62 | 1.022,16 |
| Latência p95 (ms) | 52,42 | 76,05 | 193,39 | 605,06 | 798,23 | 1.220,68 |
| Latência máxima (ms) | 72,18 | 7.105,56 | 1.286,16 | 790,63 | 4.498,05 | 8.540,59 |
| Total requisições | 207.471 | 126.465 | 148.899 | 81.504 | 51.357 | 43.401 |
| Erros | **0,00%** | **0,00%** | **0,00%** | 0,01% | 0,41% | 0,04% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.657 req/s) | Go + Gin (GORM) (4.249 req/s) | Node Fastify (3.096 req/s) | FastAPI Async (SQLAlchemy) (604 req/s) | Spring WebFlux (202 req/s) | Spring MVC (60 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.709 req/s) | Go + Gin (GORM) (4.247 req/s) | Node Fastify (3.144 req/s) | FastAPI Async (SQLAlchemy) (593 req/s) | Spring WebFlux (587 req/s) | Spring MVC (406 req/s) |
| Spike | Rust + Axum (sqlx) (2.764 req/s) | Go + Gin (GORM) (1.983 req/s) | Node Fastify (1.685 req/s) | Spring WebFlux (1.085 req/s) | Spring MVC (684 req/s) | FastAPI Async (SQLAlchemy) (578 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (7.657 req/s), menor p95 = **Rust + Axum (sqlx)** (44,01 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7.709 req/s), menor p95 = **Rust + Axum (sqlx)** (88,72 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2.764 req/s), menor p95 = **Rust + Axum (sqlx)** (52,42 ms)