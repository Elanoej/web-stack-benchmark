# Resultados v2 — 1cpus-4gb

> **Ambiente:** 1 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.709 | 4.329 | 3.513 | 1.222 | 195 | 92 | 609 |
| Latência média (ms) | 25,84 | 46,07 | 56,72 | 162,83 | 1.018,70 | 2.116,86 | 325,83 |
| Latência p50 (ms) | 35,37 | 20,65 | 46,99 | 116,49 | 989,70 | 502,44 | 484,42 |
| Latência p90 (ms) | 41,70 | 106,18 | 84,88 | 308,40 | 1.998,59 | 5.896,41 | 499,37 |
| Latência p95 (ms) | 43,83 | 160,85 | 96,78 | 408,66 | 2.701,02 | 14.225,93 | 904,88 |
| Latência máxima (ms) | 63,37 | 618,45 | 4.208,21 | 1.586,87 | 5.103,39 | 16.499,83 | 1.480,53 |
| Total requisições | 231.669 | 130.113 | 105.885 | 36.996 | 6.000 | 2.916 | 18.618 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.633 | 4.264 | 3.375 | 2.636 | 646 | 420 | 588 |
| Latência média (ms) | 28,18 | 50,58 | 63,94 | 81,96 | 337,43 | 527,16 | 374,19 |
| Latência p50 (ms) | 16,43 | 12,09 | 53,62 | 73,75 | 305,11 | 301,85 | 149,42 |
| Latência p90 (ms) | 78,49 | 126,82 | 132,68 | 161,13 | 793,66 | 1.204,82 | 1.136,27 |
| Latência p95 (ms) | 87,00 | 204,70 | 158,82 | 175,08 | 804,17 | 1.798,73 | 1.260,96 |
| Latência máxima (ms) | 109,63 | 1.697,74 | 410,72 | 270,98 | 1.097,98 | 8.704,19 | 4.754,92 |
| Total requisições | 610.614 | 341.142 | 270.042 | 210.849 | 51.711 | 33.615 | 47.079 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.750 | 1.995 | 1.727 | 1.632 | 1.244 | 681 | 579 |
| Latência média (ms) | 15,73 | 34,47 | 45,68 | 49,82 | 76,37 | 170,72 | 209,62 |
| Latência p50 (ms) | 1,92 | 1,35 | 1,98 | 1,06 | 1,59 | 7,90 | 6,87 |
| Latência p90 (ms) | 50,65 | 107,71 | 84,51 | 154,90 | 408,14 | 495,11 | 979,95 |
| Latência p95 (ms) | 56,80 | 191,77 | 105,73 | 161,33 | 485,34 | 795,98 | 1.226,83 |
| Latência máxima (ms) | 75,63 | 1.084,58 | 7.407,55 | 193,22 | 793,25 | 3.807,72 | 6.728,11 |
| Total requisições | 206.508 | 149.823 | 129.600 | 122.442 | 93.402 | 51.066 | 43.437 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º | 7º |
|---|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.709 req/s) | Go + Gin (GORM) (4.329 req/s) | Node Fastify (3.513 req/s) | Kotlin Ktor (Exposed) (1.222 req/s) | FastAPI Async (SQLAlchemy) (609 req/s) | Spring WebFlux (195 req/s) | Spring MVC (92 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.633 req/s) | Go + Gin (GORM) (4.264 req/s) | Node Fastify (3.375 req/s) | Kotlin Ktor (Exposed) (2.636 req/s) | Spring WebFlux (646 req/s) | FastAPI Async (SQLAlchemy) (588 req/s) | Spring MVC (420 req/s) |
| Spike | Rust + Axum (sqlx) (2.750 req/s) | Go + Gin (GORM) (1.995 req/s) | Node Fastify (1.727 req/s) | Kotlin Ktor (Exposed) (1.632 req/s) | Spring WebFlux (1.244 req/s) | Spring MVC (681 req/s) | FastAPI Async (SQLAlchemy) (579 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-4gb.
- **Kotlin Ktor (Exposed)** estreia como a melhor stack JVM, superando WebFlux e MVC.
- **0% de erro** em todos os cenários para todas as stacks.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (7.709 req/s), menor p95 = **Rust + Axum (sqlx)** (43,83 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (7.633 req/s), menor p95 = **Rust + Axum (sqlx)** (87,00 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (2.750 req/s), menor p95 = **Rust + Axum (sqlx)** (56,80 ms)
