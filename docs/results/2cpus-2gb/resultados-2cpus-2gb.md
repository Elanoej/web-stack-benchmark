# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, demais stacks atualizadas para 30). FastAPI com 2 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 13396.9 | 6004 | 8716.8 | 732 | 266 | 1197.7 |
| Latência média (ms) | 14.84 | 33 | 22.84 | 272.26 | 747.47 | 166.17 |
| Latência p50 (ms) | 20.46 | 29 | 15.2 | 290.15 | 107.52 | 236.23 |
| Latência p90 (ms) | 23.34 | 54 | 55.41 | 492.19 | 1692.50 | 479.32 |
| Latência p95 (ms) | 24.07 | 63 | 73.12 | 790.42 | 2468.89 | 499.75 |
| Latência máxima (ms) | 51 | 1521 | 399 | 2771 | 11397 | 1766 |
| Total requisições | 402303 | 180690 | 261993 | 22182 | 8106 | 36273 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 13374.9 | 5996 | 8667.9 | 2411 | 1021 | 1189.1 |
| Latência média (ms) | 16.03 | 36 | 24.81 | 89.58 | 212.96 | 183.31 |
| Latência p50 (ms) | 9.47 | 29 | 9.51 | 87.40 | 107.17 | 6.62 |
| Latência p90 (ms) | 43.7 | 73 | 67.25 | 211.18 | 507.23 | 558.67 |
| Latência p95 (ms) | 49.68 | 88 | 102.15 | 256.92 | 699.39 | 693.05 |
| Latência máxima (ms) | 78 | 1996 | 803 | 376 | 2801 | 4491 |
| Total requisições | 1070019 | 479667 | 693453 | 192885 | 81675 | 95133 |
| Erros | 0,29% | 0.007% | 0,08% | 0,00% | 0,00% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3770.6 | 2307 | 2941.1 | 1653 | 1802 | 1050.8 |
| Latência média (ms) | 2.44 | 25 | 12.55 | 48.67 | 41.81 | 97.35 |
| Latência p50 (ms) | 1.29 | 8 | 2.14 | 1.46 | 3.19 | 4.40 |
| Latência p90 (ms) | 6.52 | 55 | 38.6 | 201.74 | 116.31 | 515.05 |
| Latência p95 (ms) | 8.08 | 69 | 56.95 | 226.64 | 192.44 | 600.64 |
| Latência máxima (ms) | 29 | 1582 | 329 | 358 | 716 | 3019 |
| Total requisições | 282903 | 173013 | 220737 | 124104 | 135330 | 78855 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (13396.9 req/s) | Go + Gin (GORM) (8716.8 req/s) | Node Fastify (6004 req/s) | FastAPI Async (SQLAlchemy) (1197.7 req/s) | Spring WebFlux (732 req/s) | Spring MVC (266 req/s) |
| Ramp-up | Rust + Axum (sqlx) (13396.9 req/s) | Go + Gin (GORM) (8716.8 req/s) | Node Fastify (5996 req/s) | Spring WebFlux (2411 req/s) | Spring MVC (1021 req/s) | FastAPI Async (SQLAlchemy) (1189.1 req/s) |
| Spike | Rust + Axum (sqlx) (13396.9 req/s) | Go + Gin (GORM) (8716.8 req/s) | Node Fastify (2307 req/s) | Spring MVC (1802 req/s) | Spring WebFlux (1653 req/s) | FastAPI Async (SQLAlchemy) (1050.8 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-2gb.
- **Node Fastify (cluster mode)** teve o terceiro maior throughput em todos os cenários (6004 req/s steady, 5996 req/s ramp-up, 2307 req/s spike).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (12228 req/s), menor p95 = **Rust + Axum (sqlx)** (26.32 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (11860 req/s), menor p95 = **Rust + Axum (sqlx)** (55.46 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3570 req/s), menor p95 = **Rust + Axum (sqlx)** (15.06 ms)
