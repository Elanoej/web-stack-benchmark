# Resultados v2 — 1cpus-4gb

> **Ambiente:** 1 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | FastAPI Async (SQLAlchemy) | Spring MVC | Spring WebFlux |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.709 | 4.329 | 3.513 | 1.222 | 609 | 387 | 189 |
| Latência média (ms) | 25,84 | 46,07 | 56,72 | 162,83 | 325,83 | 511,74 | 1.049,65 |
| Latência p50 (ms) | 35,37 | 20,65 | 46,99 | 116,49 | 484,42 | 314,02 | 906,07 |
| Latência p90 (ms) | 41,70 | 106,18 | 84,88 | 308,40 | 499,37 | 891,92 | 2.186,75 |
| Latência p95 (ms) | 43,83 | 160,85 | 96,78 | 408,66 | 904,88 | 1.646,77 | 2.998,66 |
| Latência máxima (ms) | 63,37 | 618,45 | 4.208,21 | 1.586,87 | 1.480,53 | 6.603,61 | 5.700,54 |
| Total requisições | 231.669 | 130.113 | 105.885 | 36.996 | 18.618 | 11.904 | 5.850 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring MVC | Spring WebFlux | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.633 | 4.264 | 3.375 | 2.636 | 1.978 | 726 | 588 |
| Latência média (ms) | 28,18 | 50,58 | 63,94 | 81,96 | 109,17 | 299,49 | 374,19 |
| Latência p50 (ms) | 16,43 | 12,09 | 53,62 | 73,75 | 105,36 | 296,94 | 149,42 |
| Latência p90 (ms) | 78,49 | 126,82 | 132,68 | 161,13 | 184,02 | 692,94 | 1.136,27 |
| Latência p95 (ms) | 87,00 | 204,70 | 158,82 | 175,08 | 199,97 | 707,73 | 1.260,96 |
| Latência máxima (ms) | 109,63 | 1.697,74 | 410,72 | 270,98 | 505,90 | 1.089,11 | 4.754,92 |
| Total requisições | 610.614 | 341.142 | 270.042 | 210.849 | 158.244 | 58.062 | 47.079 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring MVC | Spring WebFlux | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.750 | 1.995 | 1.727 | 1.632 | 1.645 | 1.271 | 579 |
| Latência média (ms) | 15,73 | 34,47 | 45,68 | 49,82 | 49,13 | 74,19 | 209,62 |
| Latência p50 (ms) | 1,92 | 1,35 | 1,98 | 1,06 | 3,12 | 1,51 | 6,87 |
| Latência p90 (ms) | 50,65 | 107,71 | 84,51 | 154,90 | 178,86 | 408,10 | 979,95 |
| Latência p95 (ms) | 56,80 | 191,77 | 105,73 | 161,33 | 190,13 | 485,43 | 1.226,83 |
| Latência máxima (ms) | 75,63 | 1.084,58 | 7.407,55 | 193,22 | 395,06 | 889,16 | 6.728,11 |
| Total requisições | 206.508 | 149.823 | 129.600 | 122.442 | 123.453 | 95.430 | 43.437 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º | 7º |
|---|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.709 req/s) | Go + Gin (GORM) (4.329 req/s) | Node Fastify (3.513 req/s) | Kotlin Ktor (Exposed) (1.222 req/s) | FastAPI Async (SQLAlchemy) (609 req/s) | Spring MVC (387 req/s) | Spring WebFlux (189 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.633 req/s) | Go + Gin (GORM) (4.264 req/s) | Node Fastify (3.375 req/s) | Kotlin Ktor (Exposed) (2.636 req/s) | Spring MVC (1.978 req/s) | Spring WebFlux (726 req/s) | FastAPI Async (SQLAlchemy) (588 req/s) |
| Spike | Rust + Axum (sqlx) (2.750 req/s) | Go + Gin (GORM) (1.995 req/s) | Spring MVC (1.645 req/s) | Kotlin Ktor (Exposed) (1.632 req/s) | Node Fastify (1.727 req/s) | ... | |

Wait, I need to check the ordering more carefully for spike 1cpus:
1. Rust 2.750
2. Go 1.995
3. Node 1.727
4. Ktor 1.632
5. MVC 1.645

So MVC at 1.645 is slightly higher than Ktor at 1.632. So the order is: Rust > Go > Node > MVC > Ktor > WebFlux > FastAPI

Let me fix the podio.
<｜end▁of▁thinking｜>

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="edit">
<｜｜DSML｜｜parameter name="filePath" string="true">/home/ejnoob/temp/web-stack-benchmark/docs/v2/results/1cpus-4gb/resultados-1cpus-4gb.md