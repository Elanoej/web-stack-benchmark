# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). FastAPI com 4 workers. Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 16.476 | 11.004 | 14.176 | 3.040 | 1.162 | 2.319 |
| Latência média (ms) | 12,05 | 18,07 | 14,01 | 65,61 | 171,65 | 85,89 |
| Latência p50 (ms) | 11,97 | 16,09 | 13,21 | 59,46 | 73,81 | 4,91 |
| Latência p90 (ms) | 13,18 | 29,58 | 22,88 | 138,55 | 398,56 | 246,88 |
| Latência p95 (ms) | 13,68 | 36,86 | 28,54 | 187,05 | 583,51 | 302,00 |
| Latência máxima (ms) | 533 | 551 | 139 | 1683 | 6830 | 1084 |
| Total requisições | 494.661 | 330.666 | 425.712 | 91.515 | 35.034 | 69.969 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 15.722 | 11.071 | 13.325 | 4.919 | 5.729 | 2.272 |
| Latência média (ms) | 13,62 | 19,38 | 16,08 | 43,79 | 37,53 | 95,34 |
| Latência p50 (ms) | 12,13 | 15,06 | 12,58 | 27,82 | 28,23 | 4,72 |
| Latência p90 (ms) | 27,83 | 42,25 | 34,23 | 121,80 | 85,52 | 286,51 |
| Latência p95 (ms) | 30,07 | 51,39 | 38,84 | 133,40 | 107,07 | 417,66 |
| Latência máxima (ms) | 65 | 291 | 304 | 166 | 461 | 2576 |
| Total requisições | 1.257.753 | 885.702 | 1.066.008 | 393.513 | 458.373 | 181.800 |
| Erros | 0,00% | 0,17% | 0,00% | 0,00% | 0,06% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.836 | 3.235 | 3.651 | 2.186 | 2.654 | 1.448 |
| Latência média (ms) | 1,80 | 8,36 | 3,59 | 28,49 | 17,47 | 60,80 |
| Latência p50 (ms) | 1,23 | 4,98 | 1,77 | 1,58 | 4,20 | 2,77 |
| Latência p90 (ms) | 4,04 | 19,93 | 9,04 | 97,61 | 51,71 | 262,88 |
| Latência p95 (ms) | 5,17 | 24,79 | 11,82 | 104,07 | 81,60 | 306,93 |
| Latência máxima (ms) | 16 | 198 | 66 | 138 | 373 | 1687 |
| Total requisições | 287.937 | 242.826 | 274.011 | 164.127 | 199.287 | 108.663 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16.476 req/s) | Go + Gin (GORM) (14.176 req/s) | Node Fastify (11.004 req/s) | Spring WebFlux (3.040 req/s) | FastAPI Async (SQLAlchemy) (2.319 req/s) | Spring MVC (1.162 req/s) |
| Ramp-up | Rust + Axum (sqlx) (15.722 req/s) | Go + Gin (GORM) (13.325 req/s) | Node Fastify (11.071 req/s) | Spring MVC (5.729 req/s) | Spring WebFlux (4.919 req/s) | FastAPI Async (SQLAlchemy) (2.272 req/s) |
| Spike | Rust + Axum (sqlx) (3.836 req/s) | Go + Gin (GORM) (3.651 req/s) | Node Fastify (3.235 req/s) | Spring MVC (2.654 req/s) | Spring WebFlux (2.186 req/s) | FastAPI Async (SQLAlchemy) (1.448 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 4cpus-4gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16.476 req/s), menor p95 = **Rust + Axum (sqlx)** (13,68 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (15.722 req/s), menor p95 = **Rust + Axum (sqlx)** (30,07 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.836 req/s), menor p95 = **Rust + Axum (sqlx)** (5,17 ms)
