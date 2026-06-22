# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 3 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 12228 | 6004 | 8234 | 732 | 896 | 1798 |
| Latência média (ms) | 16.26 | 33 | 24.18 | 272.26 | 220.82 | 110.10 |
| Latência p50 (ms) | 22.73 | 29 | 14.10 | 290.15 | 15.59 | 18.49 |
| Latência p90 (ms) | 25.52 | 54 | 62.15 | 492.19 | 694.66 | 330.27 |
| Latência p95 (ms) | 26.32 | 63 | 82.67 | 790.42 | 1205.87 | 488.80 |
| Latência máxima (ms) | 76 | 1521 | 373 | 2771 | 10199 | 3363 |
| Total requisições | 367233 | 180690 | 247398 | 22182 | 27435 | 54834 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 68.48% | 57.10% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 11860 | 5996 | 8038 | 2411 | 1185 | 1055 |
| Latência média (ms) | 18.09 | 36 | 26.76 | 89.58 | 182.89 | 206.35 |
| Latência p50 (ms) | 10.82 | 29 | 9.11 | 87.40 | 132.93 | 101.87 |
| Latência p90 (ms) | 49.78 | 73 | 74.22 | 211.18 | 394.50 | 554.22 |
| Latência p95 (ms) | 55.46 | 88 | 113.61 | 256.92 | 510.32 | 720.06 |
| Latência máxima (ms) | 79 | 1996 | 1053 | 376 | 2023 | 4595 |
| Total requisições | 948804 | 479667 | 643017 | 192885 | 94776 | 84429 |
| Erros | 0.31% | 0.007% | 0.15% | 0,00% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3570 | 2307 | 2771 | 1653 | 1659 | 938 |
| Latência média (ms) | 4.44 | 25 | 15.39 | 48.67 | 48.36 | 113.26 |
| Latência p50 (ms) | 1.40 | 8 | 2.14 | 1.46 | 10.43 | 9.55 |
| Latência p90 (ms) | 12.58 | 55 | 47.53 | 201.74 | 152.88 | 503.99 |
| Latência p95 (ms) | 15.06 | 69 | 71.13 | 226.64 | 163.18 | 656.54 |
| Latência máxima (ms) | 30 | 1582 | 529 | 358 | 575 | 5665 |
| Total requisições | 267897 | 173013 | 207966 | 124104 | 124470 | 70374 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0.03% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (12228 req/s) | Go + Gin (GORM) (8234 req/s) | Node Fastify (6004 req/s) | FastAPI Async (SQLAlchemy) (1798 req/s) | Spring MVC (896 req/s) | Spring WebFlux (732 req/s) |
| Ramp-up | Rust + Axum (sqlx) (11860 req/s) | Go + Gin (GORM) (8038 req/s) | Node Fastify (5996 req/s) | Spring WebFlux (2411 req/s) | Spring MVC (1185 req/s) | FastAPI Async (SQLAlchemy) (1055 req/s) |
| Spike | Rust + Axum (sqlx) (3570 req/s) | Go + Gin (GORM) (2771 req/s) | Node Fastify (2307 req/s) | Spring MVC (1659 req/s) | Spring WebFlux (1653 req/s) | FastAPI Async (SQLAlchemy) (938 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-2gb.
- **Node Fastify (cluster mode)** teve o terceiro maior throughput em todos os cenários (6004 req/s steady, 5996 req/s ramp-up, 2307 req/s spike).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (12228 req/s), menor p95 = **Rust + Axum (sqlx)** (26.32 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (11860 req/s), menor p95 = **Rust + Axum (sqlx)** (55.46 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3570 req/s), menor p95 = **Rust + Axum (sqlx)** (15.06 ms)
