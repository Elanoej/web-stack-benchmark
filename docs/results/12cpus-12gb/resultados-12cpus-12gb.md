# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, demais stacks atualizadas para 30). FastAPI com 12 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 16396.3 | 13610 | 13500.9 | 8020 | 6284 | 5237.3 |
| Latência média (ms) | 12.1 | 15 | 14.71 | 24.82 | 31.67 | 37.90 |
| Latência p50 (ms) | 11.89 | 14 | 14.39 | 25.52 | 6.72 | 6.13 |
| Latência p90 (ms) | 13.16 | 17 | 16.02 | 53.86 | 77.72 | 102.07 |
| Latência p95 (ms) | 13.93 | 18 | 16.89 | 64.30 | 109.76 | 182.59 |
| Latência máxima (ms) | 527 | 525 | 643 | 933 | 2153 | 1992 |
| Total requisições | 492249 | 408771 | 405528 | 240897 | 188907 | 158169 |
| Erros | 0,00% | 0.28% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15922.4 | 14198 | 13153.7 | 11027 | 8061 | 4948.7 |
| Latência média (ms) | 13.44 | 15 | 16.29 | 19.44 | 26.64 | 43.57 |
| Latência p50 (ms) | 11.77 | 13 | 14.41 | 12.53 | 17.34 | 5.91 |
| Latência p90 (ms) | 27.2 | 31 | 33.15 | 51.89 | 66.84 | 139.14 |
| Latência p95 (ms) | 29.94 | 33 | 35.92 | 57.91 | 87.50 | 186.31 |
| Latência máxima (ms) | 68 | 79 | 76 | 97 | 420 | 1621 |
| Total requisições | 1273806 | 1135881 | 1052322 | 882150 | 644871 | 395925 |
| Erros | 0,00% | 0.02% | 0,00% | 0,23% | 0,13% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3843.5 | 3766 | 3733.6 | 3387 | 2850 | 2092.3 |
| Latência média (ms) | 1.74 | 2 | 2.76 | 6.47 | 13.96 | 31.38 |
| Latência p50 (ms) | 1.24 | 1.6 | 1.69 | 1.90 | 3.14 | 2.88 |
| Latência p90 (ms) | 3.89 | 6 | 6.38 | 18.19 | 39.93 | 105.80 |
| Latência p95 (ms) | 5.13 | 7 | 7.7 | 20.31 | 69.11 | 166.42 |
| Latência máxima (ms) | 14 | 24 | 37 | 36 | 431 | 1719 |
| Total requisições | 288351 | 282825 | 280290 | 254130 | 213990 | 157128 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (16396.3 req/s) | Node Fastify (13610 req/s) | Go + Gin (GORM) (13500.9 req/s) | Spring WebFlux (8020 req/s) | Spring MVC (6284 req/s) | FastAPI Async (SQLAlchemy) (5237.3 req/s) |
| Ramp-up | Rust + Axum (sqlx) (16396.3 req/s) | Node Fastify (14198 req/s) | Go + Gin (GORM) (13500.9 req/s) | Spring WebFlux (11027 req/s) | Spring MVC (8061 req/s) | FastAPI Async (SQLAlchemy) (4948.7 req/s) |
| Spike | Rust + Axum (sqlx) (16396.3 req/s) | Node Fastify (3766 req/s) | Go + Gin (GORM) (13500.9 req/s) | Spring WebFlux (3387 req/s) | Spring MVC (2850 req/s) | FastAPI Async (SQLAlchemy) (2092.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13610 req/s steady, 14198 req/s ramp-up, 3766 req/s spike), superando Go + Gin com margem expressiva.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (16396.3 req/s), menor p95 = **Rust + Axum (sqlx)** (13.93 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (15922.4 req/s), menor p95 = **Rust + Axum (sqlx)** (29.94 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3843.5 req/s), menor p95 = **Rust + Axum (sqlx)** (5.13 ms)
