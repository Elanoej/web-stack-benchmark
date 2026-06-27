# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.476 | 11.004 | 14.176 | 3.141 | 1.052 | 2.319 |
| Latência média (ms) | 12,05 | 18,07 | 14,01 | 63,48 | 189,49 | 85,89 |
| Latência p50 (ms) | 11,97 | 16,09 | 13,21 | 55,73 | 90,72 | 4,91 |
| Latência p90 (ms) | 13,18 | 29,58 | 22,88 | 138,05 | 392,52 | 246,88 |
| Latência p95 (ms) | 13,68 | 36,86 | 28,54 | 190,09 | 516,45 | 302,00 |
| Latência máxima (ms) | 532,66 | 550,80 | 139,05 | 1.297,13 | 6.332,17 | 1.084,23 |
| Total requisições | 494.661 | 330.666 | 425.712 | 94.551 | 31.746 | 69.969 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 15.722 | 11.071 | 13.325 | 5.221 | 4.836 | 2.272 |
| Latência média (ms) | 13,62 | 19,38 | 16,08 | 41,24 | 44,48 | 95,34 |
| Latência p50 (ms) | 12,13 | 15,06 | 12,58 | 26,10 | 26,16 | 4,72 |
| Latência p90 (ms) | 27,83 | 42,25 | 34,23 | 113,97 | 106,37 | 286,51 |
| Latência p95 (ms) | 30,07 | 51,39 | 38,84 | 128,86 | 150,10 | 417,66 |
| Latência máxima (ms) | 64,93 | 291,03 | 303,58 | 165,73 | 880,28 | 2.576,45 |
| Total requisições | 1.257.753 | 885.702 | 1.066.008 | 417.711 | 386.925 | 181.800 |
| Erros | **0,00%** | 0,17% | **0,00%** | 0,00% | 0,32% | **0,00%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.836 | 3.235 | 3.651 | 2.242 | 2.634 | 1.448 |
| Latência média (ms) | 1,80 | 8,36 | 3,59 | 26,93 | 17,89 | 60,80 |
| Latência p50 (ms) | 1,23 | 4,98 | 1,77 | 1,53 | 4,43 | 2,77 |
| Latência p90 (ms) | 4,04 | 19,93 | 9,04 | 91,00 | 55,93 | 262,88 |
| Latência p95 (ms) | 5,17 | 24,79 | 11,82 | 96,30 | 86,56 | 306,93 |
| Latência máxima (ms) | 15,70 | 198,06 | 66,46 | 123,14 | 630,21 | 1.687,16 |
| Total requisições | 287.937 | 242.826 | 274.011 | 168.327 | 197.568 | 108.663 |
| Erros | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.476 req/s) | Go + Gin (GORM) (14.176 req/s) | Node Fastify (11.004 req/s) | Spring WebFlux (3.141 req/s) | FastAPI Async (SQLAlchemy) (2.319 req/s) | Spring MVC (1.052 req/s) |
| Ramp-up | Rust + Axum (sqlx) (15.722 req/s) | Go + Gin (GORM) (13.325 req/s) | Node Fastify (11.071 req/s) | Spring WebFlux (5.221 req/s) | Spring MVC (4.836 req/s) | FastAPI Async (SQLAlchemy) (2.272 req/s) |
| Spike | Rust + Axum (sqlx) (3.836 req/s) | Go + Gin (GORM) (3.651 req/s) | Node Fastify (3.235 req/s) | Spring MVC (2.634 req/s) | Spring WebFlux (2.242 req/s) | FastAPI Async (SQLAlchemy) (1.448 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 4cpus-4gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.476 req/s), menor p95 = **Rust + Axum (sqlx)** (13,68 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (15.722 req/s), menor p95 = **Rust + Axum (sqlx)** (30,07 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.836 req/s), menor p95 = **Rust + Axum (sqlx)** (5,17 ms)