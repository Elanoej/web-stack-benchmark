# Resultados v2 — 2cpus-8gb

> **Ambiente:** 2 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 12.969 | 8.735 | 6.464 | 3.343 | 752 | 242 | 601 |
| Latência média (ms) | 15,33 | 22,80 | 30,82 | 59,62 | 265,08 | 817,75 | 330,29 |
| Latência p50 (ms) | 21,32 | 15,08 | 27,92 | 44,43 | 278,33 | 200,50 | 488,56 |
| Latência p90 (ms) | 24,00 | 55,24 | 48,35 | 95,27 | 498,61 | 1.695,31 | 506,54 |
| Latência p95 (ms) | 24,67 | 73,37 | 57,39 | 119,39 | 700,06 | 2.695,77 | 537,35 |
| Latência máxima (ms) | 49,72 | 287,85 | 1.394,82 | 693,07 | 3.374,17 | 12.813,73 | 1.499,01 |
| Total requisições | 389.439 | 262.473 | 194.412 | 100.662 | 22.797 | 7.428 | 18.369 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 12.825 | 8.674 | 6.139 | 5.005 | 2.580 | 1.086 | 598 |
| Latência média (ms) | 16,72 | 24,78 | 35,06 | 43,05 | 83,66 | 200,36 | 368,13 |
| Latência p50 (ms) | 9,99 | 9,55 | 28,12 | 39,18 | 85,91 | 102,03 | 157,63 |
| Latência p90 (ms) | 46,20 | 67,21 | 75,82 | 85,79 | 200,05 | 501,75 | 1.080,58 |
| Latência p95 (ms) | 52,20 | 102,36 | 92,10 | 93,29 | 212,62 | 704,26 | 1.203,16 |
| Latência máxima (ms) | 69,78 | 740,68 | 227,91 | 121,30 | 382,59 | 3.802,70 | 4.822,14 |
| Total requisições | 1.026.024 | 693.906 | 491.151 | 400.362 | 206.433 | 86.859 | 47.838 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 3.684 | 2.952 | 2.324 | 2.203 | 1.732 | 1.807 | 579 |
| Latência média (ms) | 3,29 | 12,38 | 24,81 | 28,05 | 44,94 | 41,56 | 208,47 |
| Latência p50 (ms) | 1,30 | 2,11 | 9,50 | 8,68 | 1,47 | 3,45 | 7,05 |
| Latência p90 (ms) | 9,46 | 38,11 | 63,00 | 68,58 | 185,76 | 111,23 | 987,14 |
| Latência p95 (ms) | 11,88 | 56,44 | 75,06 | 72,36 | 192,41 | 200,34 | 1.212,53 |
| Latência máxima (ms) | 27,51 | 364,69 | 955,44 | 93,24 | 357,19 | 1.017,04 | 7.244,77 |
| Total requisições | 276.297 | 221.544 | 174.438 | 165.264 | 130.008 | 135.744 | 43.479 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º | 7º |
|---|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (12.969 req/s) | Go + Gin (GORM) (8.735 req/s) | Node Fastify (6.464 req/s) | Kotlin Ktor (Exposed) (3.343 req/s) | Spring WebFlux (752 req/s) | FastAPI Async (SQLAlchemy) (601 req/s) | Spring MVC (242 req/s) |
| Ramp-up | Rust + Axum (sqlx) (12.825 req/s) | Go + Gin (GORM) (8.674 req/s) | Node Fastify (6.139 req/s) | Kotlin Ktor (Exposed) (5.005 req/s) | Spring WebFlux (2.580 req/s) | Spring MVC (1.086 req/s) | FastAPI Async (SQLAlchemy) (598 req/s) |
| Spike | Rust + Axum (sqlx) (3.684 req/s) | Go + Gin (GORM) (2.952 req/s) | Node Fastify (2.324 req/s) | Kotlin Ktor (Exposed) (2.203 req/s) | Spring MVC (1.807 req/s) | Spring WebFlux (1.732 req/s) | FastAPI Async (SQLAlchemy) (579 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-8gb.
- **Kotlin Ktor (Exposed)** estreia como a melhor stack JVM, superando WebFlux e MVC.
- **0% de erro** em todos os cenários para todas as stacks.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (12.969 req/s), menor p95 = **Rust + Axum (sqlx)** (24,67 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (12.825 req/s), menor p95 = **Rust + Axum (sqlx)** (52,20 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (3.684 req/s), menor p95 = **Rust + Axum (sqlx)** (11,88 ms)
