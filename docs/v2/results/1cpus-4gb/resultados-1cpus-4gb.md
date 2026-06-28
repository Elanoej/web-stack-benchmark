# Resultados v2 — 1cpus-4gb

> **Ambiente:** 1 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Native Query) | FastAPI Async (SQLAlchemy) | Spring MVC | Spring WebFlux |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.709 | 4.329 | 3.513 | **1.472** | 609 | 387 | 189 |
| Latência média (ms) | 25,84 | 46,07 | 56,72 | **135,31** | 325,83 | 511,74 | 1.049,65 |
| Latência p50 (ms) | 35,37 | 20,65 | 46,99 | **104,10** | 484,42 | 314,02 | 906,07 |
| Latência p90 (ms) | 41,70 | 106,18 | 84,88 | **277,14** | 499,37 | 891,92 | 2.186,75 |
| Latência p95 (ms) | 43,83 | 160,85 | 96,78 | **319,78** | 904,88 | 1.646,77 | 2.998,66 |
| Latência máxima (ms) | 63,37 | 618,45 | 4.208,21 | **1.093,90** | 1.480,53 | 6.603,61 | 5.700,54 |
| Total requisições | 231.669 | 130.113 | 105.885 | **44.427** | 18.618 | 11.904 | 5.850 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Native Query) | Spring MVC | Spring WebFlux | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.633 | 4.264 | 3.375 | **2.753** | 1.978 | 726 | 588 |
| Latência média (ms) | 28,18 | 50,58 | 63,94 | **78,45** | 109,17 | 299,49 | 374,19 |
| Latência p50 (ms) | 16,43 | 12,09 | 53,62 | **70,27** | 105,36 | 296,94 | 149,42 |
| Latência p90 (ms) | 78,49 | 126,82 | 132,68 | **154,51** | 184,02 | 692,94 | 1.136,27 |
| Latência p95 (ms) | 87,00 | 204,70 | 158,82 | **168,72** | 199,97 | 707,73 | 1.260,96 |
| Latência máxima (ms) | 109,63 | 1.697,74 | 410,72 | **240,72** | 505,90 | 1.089,11 | 4.754,92 |
| Total requisições | 610.614 | 341.142 | 270.042 | **220.266** | 158.244 | 58.062 | 47.079 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Native Query) | Spring MVC | Spring WebFlux | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.750 | 1.995 | 1.727 | **1.683** | 1.645 | 1.271 | 579 |
| Latência média (ms) | 15,73 | 34,47 | 45,68 | **47,27** | 49,13 | 74,19 | 209,62 |
| Latência p50 (ms) | 1,92 | 1,35 | 1,98 | **1,22** | 3,12 | 1,51 | 6,87 |
| Latência p90 (ms) | 50,65 | 107,71 | 84,51 | **140,63** | 178,86 | 408,10 | 979,95 |
| Latência p95 (ms) | 56,80 | 191,77 | 105,73 | **144,82** | 190,13 | 485,43 | 1.226,83 |
| Latência máxima (ms) | 75,63 | 1.084,58 | 7.407,55 | **166,91** | 395,06 | 889,16 | 6.728,11 |
| Total requisições | 206.508 | 149.823 | 129.600 | **126.249** | 123.453 | 95.430 | 43.437 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º | 7º |
|---|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.709 req/s) | Go + Gin (GORM) (4.329 req/s) | Node Fastify (3.513 req/s) | Kotlin Ktor (Native Query) (1.472 req/s) | FastAPI Async (SQLAlchemy) (609 req/s) | Spring MVC (387 req/s) | Spring WebFlux (189 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.633 req/s) | Go + Gin (GORM) (4.264 req/s) | Node Fastify (3.375 req/s) | Kotlin Ktor (Native Query) (2.753 req/s) | Spring MVC (1.978 req/s) | Spring WebFlux (726 req/s) | FastAPI Async (SQLAlchemy) (588 req/s) |
| Spike | Rust + Axum (sqlx) (2.750 req/s) | Go + Gin (GORM) (1.995 req/s) | Node Fastify (1.727 req/s) | Kotlin Ktor (Native Query) (1.683 req/s) | Spring MVC (1.645 req/s) | Spring WebFlux (1.271 req/s) | FastAPI Async (SQLAlchemy) (579 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-4gb.
- **Kotlin Ktor** com native query alcançou 1.472 req/s (steady) e 2.753 req/s (ramp-up), com ganho de +20% sobre Exposed DSL.
- **Spring MVC** com native query superou o **Spring WebFlux** em todos os cenários.
- **0% de erro** em todos os cenários para todas as stacks.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (7.709 req/s), menor p95 = **Rust + Axum (sqlx)** (43,83 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (7.633 req/s), menor p95 = **Rust + Axum (sqlx)** (87,00 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (2.750 req/s), menor p95 = **Rust + Axum (sqlx)** (56,80 ms)
