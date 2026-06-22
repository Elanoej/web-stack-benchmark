# Resultados — 12cpus-12gb

> **Ambiente:** 12 CPUs, 12GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 13 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 15076 | 13610 | 11137 | 8020 | 2580 | 1529 |
| Latência média (ms) | 13.17 | 15 | 17.83 | 24.82 | 77.14 | 130.00 |
| Latência p50 (ms) | 12.90 | 14 | 17.18 | 25.52 | 91.27 | 99.32 |
| Latência p90 (ms) | 14.35 | 17 | 19.53 | 53.86 | 149.45 | 272.34 |
| Latência p95 (ms) | 15.23 | 18 | 21.48 | 64.30 | 218.36 | 327.46 |
| Latência máxima (ms) | 529 | 525 | 651 | 933 | 1041 | 1630 |
| Total requisições | 452622 | 408771 | 334527 | 240897 | 77841 | 46308 |
| Erros | 0,00% | 0.28% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 14578 | 14198 | 10958 | 11027 | 3046 | 1584 |
| Latência média (ms) | 14.69 | 15 | 19.56 | 19.44 | 70.84 | 137.08 |
| Latência p50 (ms) | 12.96 | 13 | 17.50 | 12.53 | 57.84 | 67.09 |
| Latência p90 (ms) | 29.84 | 31 | 39.85 | 51.89 | 165.12 | 406.67 |
| Latência p95 (ms) | 32.18 | 33 | 43.28 | 57.91 | 185.02 | 503.47 |
| Latência máxima (ms) | 74 | 79 | 98 | 97 | 524 | 3203 |
| Total requisições | 1166301 | 1135881 | 876630 | 882150 | 243699 | 126702 |
| Erros | 0,00% | 0.02% | 0,00% | 0,23% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 3777 | 3766 | 3379 | 3387 | 1644 | 1211 |
| Latência média (ms) | 2.35 | 2 | 6.54 | 6.47 | 49.07 | 79.36 |
| Latência p50 (ms) | 1.49 | 1.6 | 4.77 | 1.90 | 10.86 | 6.23 |
| Latência p90 (ms) | 5.49 | 6 | 14.77 | 18.19 | 156.47 | 360.01 |
| Latência p95 (ms) | 6.69 | 7 | 16.67 | 20.31 | 165.87 | 419.73 |
| Latência máxima (ms) | 16 | 24 | 50 | 36 | 550 | 2484 |
| Total requisições | 283449 | 282825 | 253650 | 254130 | 123450 | 90846 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (15076 req/s) | Node Fastify (13610 req/s) | Go + Gin (GORM) (11137 req/s) | Spring WebFlux (8020 req/s) | Spring MVC (2580 req/s) | FastAPI Async (SQLAlchemy) (1529 req/s) |
| Ramp-up | Rust + Axum (sqlx) (14578 req/s) | Node Fastify (14198 req/s) | Go + Gin (GORM) (10958 req/s) | Spring WebFlux (11027 req/s) | Spring MVC (3046 req/s) | FastAPI Async (SQLAlchemy) (1584 req/s) |
| Spike | Rust + Axum (sqlx) (3777 req/s) | Node Fastify (3766 req/s) | Go + Gin (GORM) (3379 req/s) | Spring WebFlux (3387 req/s) | Spring MVC (1644 req/s) | FastAPI Async (SQLAlchemy) (1211 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 12cpus-12gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em todos os cenários (13610 req/s steady, 14198 req/s ramp-up, 3766 req/s spike), superando Go + Gin com margem expressiva.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (15076 req/s), menor p95 = **Rust + Axum (sqlx)** (15.23 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (14578 req/s), menor p95 = **Rust + Axum (sqlx)** (32.18 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3777 req/s), menor p95 = **Rust + Axum (sqlx)** (6.69 ms)
