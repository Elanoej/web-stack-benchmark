# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 9 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15332 | 13577 | 11281 | 4235 | 2464 | 2287 |
| Latência média (ms) | 12.95 | 15 | 17.61 | 47.07 | 80.79 | 86.85 |
| Latência p50 (ms) | 12.70 | 14 | 16.86 | 40.13 | 90.23 | 19.28 |
| Latência p90 (ms) | 14.05 | 17 | 19.74 | 92.96 | 191.14 | 254.68 |
| Latência p95 (ms) | 14.97 | 21 | 22.66 | 103.94 | 218.70 | 324.15 |
| Latência máxima (ms) | 460 | 471 | 507 | 1141 | 1571 | 2001 |
| Total requisições | 460356 | 407676 | 338850 | 127269 | 74358 | 69420 |
| Erros | 0,00% | 0.79% | 0,00% | 0,00% | 0,00% | 43.37% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14762 | 14245 | 10921 | 7629 | 3062 | 1626 |
| Latência média (ms) | 14.51 | 15 | 19.63 | 28.17 | 70.46 | 133.36 |
| Latência p50 (ms) | 12.63 | 13 | 17.16 | 18.02 | 55.46 | 66.54 |
| Latência p90 (ms) | 29.79 | 31 | 40.53 | 78.25 | 166.06 | 350.43 |
| Latência p95 (ms) | 32.21 | 33 | 44.44 | 87.67 | 189.63 | 454.96 |
| Latência máxima (ms) | 73 | 74 | 97 | 134 | 650 | 2626 |
| Total requisições | 1180959 | 1139676 | 873681 | 610350 | 244989 | 130056 |
| Erros | 0,00% | 0.03% | 0,00% | 0.12% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3778 | 3730 | 3390 | 2792 | 1643 | 1237 |
| Latência média (ms) | 2.31 | 3 | 6.41 | 15.02 | 49.10 | 76.85 |
| Latência p50 (ms) | 1.47 | 1.6 | 5.38 | 1.88 | 10.69 | 5.98 |
| Latência p90 (ms) | 5.33 | 7 | 14.16 | 46.02 | 156.69 | 363.17 |
| Latência p95 (ms) | 6.56 | 9 | 15.93 | 49.11 | 167.95 | 409.51 |
| Latência máxima (ms) | 20 | 33 | 49 | 81 | 518 | 2979 |
| Total requisições | 283722 | 279924 | 254529 | 209427 | 123393 | 92904 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (15332 req/s) | Node Fastify (13577 req/s) | Go + Gin (GORM) (11281 req/s) | Spring WebFlux (4235 req/s) | Spring MVC (2464 req/s) | FastAPI Async (SQLAlchemy) (2287 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14762 req/s) | Node Fastify (14245 req/s) | Go + Gin (GORM) (10921 req/s) | Spring WebFlux (7629 req/s) | Spring MVC (3062 req/s) | FastAPI Async (SQLAlchemy) (1626 req/s) |
| Spike | Rust + Axum (sqlx) (3778 req/s) | Node Fastify (3730 req/s) | Go + Gin (GORM) (3390 req/s) | Spring WebFlux (2792 req/s) | Spring MVC (1643 req/s) | FastAPI Async (SQLAlchemy) (1237 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13577 req/s steady, 14245 req/s ramp-up, 3730 req/s spike), superando Go + Gin em todas as cargas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15332 req/s), menor p95 = **Rust + Axum (sqlx)** (14.97 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14762 req/s), menor p95 = **Rust + Axum (sqlx)** (32.21 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3778 req/s), menor p95 = **Rust + Axum (sqlx)** (6.56 ms)
