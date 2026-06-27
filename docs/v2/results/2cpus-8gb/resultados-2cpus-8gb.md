# Resultados v2 — 2cpus-8gb

> **Ambiente:** 2 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 13.152 | 6.321 | 8.504 | 743,2692690947448 | 179,2271236178084 | 599,4655834289185 |
| Latência média (ms) | 15,11 | 31,53 | 23,42 | 267,42 | 1.104,48 | 330,93 |
| Latência p50 (ms) | 20,91 | 28,16 | 15,55 | 280,35 | 247,49 | 489,93 |
| Latência p90 (ms) | 23,67 | 50,36 | 56,83 | 493,93 | 2.101,43 | 508,77 |
| Latência p95 (ms) | 24,47 | 61,51 | 75,12 | 686,56 | 3.602,51 | 903,92 |
| Latência máxima (ms) | 66,07 | 1.384,04 | 392,65 | 2.114,31 | 15.104,77 | 1.548,35 |
| Total requisições | 394.974 | 190.029 | 255.513 | 22.581 | 5.514 | 18.327 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 12.885 | 6.096 | 8.476 | 2.632 | 953,7516322022059 | 602,737309781229 |
| Latência média (ms) | 16,64 | 35,33 | 25,37 | 82,02 | 228,51 | 364,50 |
| Latência p50 (ms) | 10,03 | 28,29 | 9,83 | 78,66 | 106,66 | 159,49 |
| Latência p90 (ms) | 46,08 | 73,51 | 68,79 | 202,07 | 594,30 | 1.064,64 |
| Latência p95 (ms) | 52,63 | 87,54 | 104,70 | 212,49 | 802,70 | 1.213,13 |
| Latência máxima (ms) | 68,48 | 1.740,37 | 798,71 | 384,99 | 3.109,79 | 4.774,17 |
| Total requisições | 1.030.812 | 487.713 | 678.069 | 210.600 | 76.320 | 48.222 |
| Erros | **0,000%** | 0,006% | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.698 | 2.253 | 2.932 | 1.719 | 1.813 | 588,7250795621545 |
| Latência média (ms) | 3,12 | 26,75 | 12,71 | 45,52 | 41,27 | 204,40 |
| Latência p50 (ms) | 1,31 | 7,96 | 2,09 | 1,47 | 3,45 | 7,20 |
| Latência p90 (ms) | 8,51 | 50,07 | 39,30 | 190,30 | 110,32 | 1.002,01 |
| Latência p95 (ms) | 11,06 | 60,74 | 58,09 | 197,24 | 199,88 | 1.199,49 |
| Latência máxima (ms) | 39,17 | 1.672,74 | 349,57 | 296,86 | 1.420,85 | 7.234,35 |
| Total requisições | 277.572 | 169.098 | 219.972 | 128.973 | 136.146 | 44.166 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (13.152 req/s) | Go + Gin (GORM) (8.504 req/s) | Node Fastify (6.321 req/s) | Spring WebFlux (743 req/s) | FastAPI Async (SQLAlchemy) (599 req/s) | Spring MVC (179 req/s) |
| Ramp-up | Rust + Axum (sqlx) (12.885 req/s) | Go + Gin (GORM) (8.476 req/s) | Node Fastify (6.096 req/s) | Spring WebFlux (2.632 req/s) | Spring MVC (954 req/s) | FastAPI Async (SQLAlchemy) (603 req/s) |
| Spike | Rust + Axum (sqlx) (3.698 req/s) | Go + Gin (GORM) (2.932 req/s) | Node Fastify (2.253 req/s) | Spring MVC (1.813 req/s) | Spring WebFlux (1.719 req/s) | FastAPI Async (SQLAlchemy) (589 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-8gb.
- Todas as stacks com **0% de erro** em steady state.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (13.152 req/s), menor p95 = **Rust + Axum (sqlx)** (24,47 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (12.885 req/s), menor p95 = **Rust + Axum (sqlx)** (52,63 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (3.698 req/s), menor p95 = **Rust + Axum (sqlx)** (11,06 ms)