# Resultados — 8cpus-8gb

> **Ambiente:** 8 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, demais stacks atualizadas para 30). FastAPI com 8 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 16644.6 | 13577 | 13296.1 | 6112 | 4412 | 4020.9 |
| Latência média (ms) | 11.92 | 15 | 14.94 | 32.60 | 45.15 | 49.50 |
| Latência p50 (ms) | 11.71 | 14 | 14.57 | 32.77 | 7.57 | 5.53 |
| Latência p90 (ms) | 12.95 | 17 | 16.6 | 74.61 | 111.91 | 135.93 |
| Latência p95 (ms) | 13.74 | 21 | 17.52 | 87.19 | 158.03 | 192.65 |
| Latência máxima (ms) | 529 | 471 | 626 | 1218 | 3536 | 1007 |
| Total requisições | 499728 | 407676 | 399345 | 183621 | 132612 | 121158 |
| Erros | 0,00% | 0.79% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 16093.8 | 14245 | 13251.0 | 8638 | 7889 | 3815.5 |
| Latência média (ms) | 13.3 | 15 | 16.17 | 24.87 | 27.22 | 56.67 |
| Latência p50 (ms) | 11.66 | 13 | 14.52 | 15.81 | 17.87 | 5.19 |
| Latência p90 (ms) | 27.15 | 31 | 32.69 | 67.81 | 67.66 | 179.95 |
| Latência p95 (ms) | 29.6 | 33 | 35.48 | 76.46 | 88.93 | 264.25 |
| Latência máxima (ms) | 59 | 74 | 80 | 99 | 385 | 1953 |
| Total requisições | 1287516 | 1139676 | 1060089 | 691020 | 631143 | 305247 |
| Erros | 0,00% | 0.03% | 0,00% | 0,03% | 0,03% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3848.1 | 3730 | 3745.1 | 2993 | 2838 | 1855.3 |
| Latência média (ms) | 1.69 | 3 | 2.64 | 11.72 | 14.15 | 39.75 |
| Latência p50 (ms) | 1.21 | 1.6 | 1.59 | 1.81 | 3.28 | 2.79 |
| Latência p90 (ms) | 3.72 | 7 | 6.35 | 35.02 | 40.37 | 146.54 |
| Latência p95 (ms) | 4.78 | 9 | 7.91 | 37.70 | 69.92 | 209.65 |
| Latência máxima (ms) | 18 | 33 | 31 | 55 | 438 | 1766 |
| Total requisições | 288801 | 279924 | 281238 | 224730 | 213099 | 139179 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16644.6 req/s) | Node Fastify (13577 req/s) | Go + Gin (GORM) (13296.1 req/s) | Spring WebFlux (6112 req/s) | Spring MVC (4412 req/s) | FastAPI Async (SQLAlchemy) (4020.9 req/s) |
| Ramp-up | Rust + Axum (sqlx) (16644.6 req/s) | Node Fastify (14245 req/s) | Go + Gin (GORM) (13296.1 req/s) | Spring WebFlux (8638 req/s) | Spring MVC (7889 req/s) | FastAPI Async (SQLAlchemy) (3815.5 req/s) |
| Spike | Rust + Axum (sqlx) (16644.6 req/s) | Node Fastify (3730 req/s) | Go + Gin (GORM) (13296.1 req/s) | Spring WebFlux (2993 req/s) | Spring MVC (2838 req/s) | FastAPI Async (SQLAlchemy) (1855.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 8cpus-8gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13577 req/s steady, 14245 req/s ramp-up, 3730 req/s spike), superando Go + Gin em todas as cargas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15332 req/s), menor p95 = **Rust + Axum (sqlx)** (14.97 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14762 req/s), menor p95 = **Rust + Axum (sqlx)** (32.21 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3778 req/s), menor p95 = **Rust + Axum (sqlx)** (6.56 ms)
