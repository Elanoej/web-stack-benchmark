# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). FastAPI com 2 workers. Node Fastify com cluster mode (workers = CPUs). PostgreSQL max_connections=30
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 13.397 | 6.219 | 8.717 | 732,3 | 265,5 | 1.198 |
| Latência média (ms) | 14,84 | 32,04 | 22,84 | 272,26 | 747,47 | 166,17 |
| Latência p50 (ms) | 20,46 | 28,81 | 15,20 | 290,15 | 107,52 | 236,23 |
| Latência p90 (ms) | 23,34 | 52,46 | 55,41 | 492,19 | 1.692,50 | 479,32 |
| Latência p95 (ms) | 24,07 | 61,78 | 73,12 | 790,42 | 2.468,89 | 499,75 |
| Latência máxima (ms) | 51 | 1429 | 399 | 2771 | 11397 | 1766 |
| Total requisições | 402.303 | 187.032 | 261.993 | 22.182 | 8.106 | 36.273 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 13.375 | 5.993 | 8.668 | 2.411 | 1.021 | 1.189 |
| Latência média (ms) | 16,03 | 35,93 | 24,81 | 89,58 | 212,96 | 183,31 |
| Latência p50 (ms) | 9,47 | 28,64 | 9,51 | 87,40 | 107,17 | 6,62 |
| Latência p90 (ms) | 43,70 | 74,74 | 67,25 | 211,18 | 507,23 | 558,67 |
| Latência p95 (ms) | 49,68 | 88,85 | 102,15 | 256,92 | 699,39 | 693,05 |
| Latência máxima (ms) | 78 | 1702 | 803 | 376 | 2801 | 4491 |
| Total requisições | 1.070.019 | 479.484 | 693.453 | 192.885 | 81.675 | 95.133 |
| Erros | 0,29% | 0,01% | 0,08% | 0,00% | 0,00% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.771 | 2.310 | 2.941 | 1.653 | 1.802 | 1.051 |
| Latência média (ms) | 2,44 | 25,24 | 12,55 | 48,67 | 41,81 | 97,35 |
| Latência p50 (ms) | 1,29 | 7,53 | 2,14 | 1,46 | 3,19 | 4,40 |
| Latência p90 (ms) | 6,52 | 47,30 | 38,60 | 201,74 | 116,31 | 515,05 |
| Latência p95 (ms) | 8,08 | 57,94 | 56,95 | 226,64 | 192,44 | 600,64 |
| Latência máxima (ms) | 29 | 1473 | 329 | 358 | 716 | 3019 |
| Total requisições | 282.903 | 173.307 | 220.737 | 124.104 | 135.330 | 78.855 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (13.397 req/s) | Go + Gin (GORM) (8.717 req/s) | Node Fastify (6.219 req/s) | FastAPI Async (SQLAlchemy) (1.198 req/s) | Spring WebFlux (732,3 req/s) | Spring MVC (265,5 req/s) |
| Ramp-up | Rust + Axum (sqlx) (13.375 req/s) | Go + Gin (GORM) (8.668 req/s) | Node Fastify (5.993 req/s) | Spring WebFlux (2.411 req/s) | FastAPI Async (SQLAlchemy) (1.189 req/s) | Spring MVC (1.021 req/s) |
| Spike | Rust + Axum (sqlx) (3.771 req/s) | Go + Gin (GORM) (2.941 req/s) | Node Fastify (2.310 req/s) | Spring MVC (1.802 req/s) | Spring WebFlux (1.653 req/s) | FastAPI Async (SQLAlchemy) (1.051 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-2gb.
- **Node Fastify (cluster mode)** competitivo com Rust Axum em cargas altas.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (13.397 req/s), menor p95 = **Rust + Axum (sqlx)** (24,07 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (13.375 req/s), menor p95 = **Rust + Axum (sqlx)** (49,68 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3.771 req/s), menor p95 = **Rust + Axum (sqlx)** (8,08 ms)
