# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 9 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15332 | 13577 | 11281 | 6112 | 4412 | 2287 |
| Latência média (ms) | 12.95 | 15 | 17.61 | 32.60 | 45.15 | 86.85 |
| Latência p50 (ms) | 12.70 | 14 | 16.86 | 32.77 | 7.57 | 19.28 |
| Latência p90 (ms) | 14.05 | 17 | 19.74 | 74.61 | 111.91 | 254.68 |
| Latência p95 (ms) | 14.97 | 21 | 22.66 | 87.19 | 158.03 | 324.15 |
| Latência máxima (ms) | 460 | 471 | 507 | 1218 | 3536 | 2001 |
| Total requisições | 460356 | 407676 | 338850 | 183621 | 132612 | 69420 |
| Erros | 0,00% | 0.79% | 0,00% | 0,00% | 0,00% | 43.37% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14762 | 14245 | 10921 | 8638 | 7889 | 1626 |
| Latência média (ms) | 14.51 | 15 | 19.63 | 24.87 | 27.22 | 133.36 |
| Latência p50 (ms) | 12.63 | 13 | 17.16 | 15.81 | 17.87 | 66.54 |
| Latência p90 (ms) | 29.79 | 31 | 40.53 | 67.81 | 67.66 | 350.43 |
| Latência p95 (ms) | 32.21 | 33 | 44.44 | 76.46 | 88.93 | 454.96 |
| Latência máxima (ms) | 73 | 74 | 97 | 99 | 385 | 2626 |
| Total requisições | 1180959 | 1139676 | 873681 | 691020 | 631143 | 130056 |
| Erros | 0,00% | 0.03% | 0,00% | 0,03% | 0,03% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3778 | 3730 | 3390 | 2993 | 2838 | 1237 |
| Latência média (ms) | 2.31 | 3 | 6.41 | 11.72 | 14.15 | 76.85 |
| Latência p50 (ms) | 1.47 | 1.6 | 5.38 | 1.81 | 3.28 | 5.98 |
| Latência p90 (ms) | 5.33 | 7 | 14.16 | 35.02 | 40.37 | 363.17 |
| Latência p95 (ms) | 6.56 | 9 | 15.93 | 37.70 | 69.92 | 409.51 |
| Latência máxima (ms) | 20 | 33 | 49 | 55 | 438 | 2979 |
| Total requisições | 283722 | 279924 | 254529 | 224730 | 213099 | 92904 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (15332 req/s) | Node Fastify (13577 req/s) | Go + Gin (GORM) (11281 req/s) | Spring WebFlux (6112 req/s) | Spring MVC (4412 req/s) | FastAPI Async (SQLAlchemy) (2287 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14762 req/s) | Node Fastify (14245 req/s) | Go + Gin (GORM) (10921 req/s) | Spring WebFlux (8638 req/s) | Spring MVC (7889 req/s) | FastAPI Async (SQLAlchemy) (1626 req/s) |
| Spike | Rust + Axum (sqlx) (3778 req/s) | Node Fastify (3730 req/s) | Go + Gin (GORM) (3390 req/s) | Spring WebFlux (2993 req/s) | Spring MVC (2838 req/s) | FastAPI Async (SQLAlchemy) (1237 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13577 req/s steady, 14245 req/s ramp-up, 3730 req/s spike), superando Go + Gin em todas as cargas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15332 req/s), menor p95 = **Rust + Axum (sqlx)** (14.97 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14762 req/s), menor p95 = **Rust + Axum (sqlx)** (32.21 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3778 req/s), menor p95 = **Rust + Axum (sqlx)** (6.56 ms)
