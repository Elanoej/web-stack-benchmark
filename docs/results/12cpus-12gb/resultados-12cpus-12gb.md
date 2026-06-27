# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=2 + max_overflow=0). FastAPI com 12 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15076 | 13610 | 11137 | 8020 | 6284 | 5237.3 |
| Latência média (ms) | 13.17 | 15 | 17.83 | 24.82 | 31.67 | 37.90 |
| Latência p50 (ms) | 12.90 | 14 | 17.18 | 25.52 | 6.72 | 6.13 |
| Latência p90 (ms) | 14.35 | 17 | 19.53 | 53.86 | 77.72 | 102.07 |
| Latência p95 (ms) | 15.23 | 18 | 21.48 | 64.30 | 109.76 | 182.59 |
| Latência máxima (ms) | 529 | 525 | 651 | 933 | 2153 | 1992 |
| Total requisições | 452622 | 408771 | 334527 | 240897 | 188907 | 158169 |
| Erros | 0,00% | 0.28% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14578 | 14198 | 10958 | 11027 | 8061 | 4948.7 |
| Latência média (ms) | 14.69 | 15 | 19.56 | 19.44 | 26.64 | 43.57 |
| Latência p50 (ms) | 12.96 | 13 | 17.50 | 12.53 | 17.34 | 5.91 |
| Latência p90 (ms) | 29.84 | 31 | 39.85 | 51.89 | 66.84 | 139.14 |
| Latência p95 (ms) | 32.18 | 33 | 43.28 | 57.91 | 87.50 | 186.31 |
| Latência máxima (ms) | 74 | 79 | 98 | 97 | 420 | 1621 |
| Total requisições | 1166301 | 1135881 | 876630 | 882150 | 644871 | 395925 |
| Erros | 0,00% | 0.02% | 0,00% | 0,23% | 0,13% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3777 | 3766 | 3379 | 3387 | 2850 | 2092.3 |
| Latência média (ms) | 2.35 | 2 | 6.54 | 6.47 | 13.96 | 31.38 |
| Latência p50 (ms) | 1.49 | 1.6 | 4.77 | 1.90 | 3.14 | 2.88 |
| Latência p90 (ms) | 5.49 | 6 | 14.77 | 18.19 | 39.93 | 105.80 |
| Latência p95 (ms) | 6.69 | 7 | 16.67 | 20.31 | 69.11 | 166.42 |
| Latência máxima (ms) | 16 | 24 | 50 | 36 | 431 | 1719 |
| Total requisições | 283449 | 282825 | 253650 | 254130 | 213990 | 157128 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (15076 req/s) | Node Fastify (13610 req/s) | Go + Gin (GORM) (11137 req/s) | Spring WebFlux (8020 req/s) | Spring MVC (6284 req/s) | FastAPI Async (SQLAlchemy) (5237.3 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14578 req/s) | Node Fastify (14198 req/s) | Go + Gin (GORM) (10958 req/s) | Spring WebFlux (11027 req/s) | Spring MVC (8061 req/s) | FastAPI Async (SQLAlchemy) (4948.7 req/s) |
| Spike | Rust + Axum (sqlx) (3777 req/s) | Node Fastify (3766 req/s) | Go + Gin (GORM) (3379 req/s) | Spring WebFlux (3387 req/s) | Spring MVC (2850 req/s) | FastAPI Async (SQLAlchemy) (2092.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13610 req/s steady, 14198 req/s ramp-up, 3766 req/s spike), superando Go + Gin com margem expressiva.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15076 req/s), menor p95 = **Rust + Axum (sqlx)** (15.23 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14578 req/s), menor p95 = **Rust + Axum (sqlx)** (32.18 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3777 req/s), menor p95 = **Rust + Axum (sqlx)** (6.69 ms)
