# Resultados v2 — 1cpus-4gb

> **Ambiente:** 1 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.541 | 3.335 | 4.251 | 168,19827532501398 | 46,09824517414613 | 606,3046442891913 |
| Latência média (ms) | 26,42 | 59,73 | 46,92 | 1.173,07 | 4.214,40 | 327,23 |
| Latência p50 (ms) | 36,02 | 45,94 | 21,31 | 999,99 | 712,23 | 484,86 |
| Latência p90 (ms) | 43,04 | 84,30 | 107,37 | 2.498,43 | 19.398,19 | 503,97 |
| Latência p95 (ms) | 44,88 | 97,46 | 164,50 | 3.289,20 | 20.200,18 | 965,71 |
| Latência máxima (ms) | 60,87 | 4.272,42 | 600,94 | 5.285,99 | 21.298,13 | 1.951,00 |
| Total requisições | 226.686 | 100.575 | 127.842 | 5.280 | 1.485 | 18.546 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 7.674 | 3.284 | 4.172 | 650,4906907465462 | 427,7142741408709 | 601,8227251317335 |
| Latência média (ms) | 28,02 | 67,80 | 51,71 | 335,01 | 516,05 | 365,38 |
| Latência p50 (ms) | 16,05 | 39,83 | 12,43 | 308,74 | 305,68 | 149,06 |
| Latência p90 (ms) | 78,22 | 76,10 | 130,71 | 788,56 | 1.198,91 | 1.076,56 |
| Latência p95 (ms) | 87,96 | 89,28 | 207,46 | 801,60 | 1.696,73 | 1.201,02 |
| Latência máxima (ms) | 126,09 | 8.853,43 | 1.498,78 | 1.100,10 | 6.413,53 | 4.863,75 |
| Total requisições | 613.938 | 262.755 | 333.735 | 52.041 | 34.233 | 48.147 |
| Erros | **0,000%** | 0,002% | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput (req/s) | 2.772 | 1.692 | 1.990 | 1.244 | 652,4667178315325 | 586,2995892665832 |
| Latência média (ms) | 15,36 | 48,31 | 34,70 | 76,48 | 180,24 | 205,77 |
| Latência p50 (ms) | 1,89 | 1,80 | 1,36 | 1,50 | 87,44 | 7,11 |
| Latência p90 (ms) | 49,24 | 57,12 | 107,95 | 414,41 | 498,65 | 973,33 |
| Latência p95 (ms) | 54,38 | 71,91 | 191,94 | 492,35 | 799,38 | 1.201,04 |
| Latência máxima (ms) | 76,53 | 6.922,02 | 1.116,04 | 902,37 | 5.004,89 | 6.640,28 |
| Total requisições | 208.083 | 127.080 | 149.373 | 93.327 | 48.963 | 44.013 |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.541 req/s) | Go + Gin (GORM) (4.251 req/s) | Node Fastify (3.335 req/s) | FastAPI Async (SQLAlchemy) (606 req/s) | Spring WebFlux (168 req/s) | Spring MVC (46 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.674 req/s) | Go + Gin (GORM) (4.172 req/s) | Node Fastify (3.284 req/s) | Spring WebFlux (650 req/s) | FastAPI Async (SQLAlchemy) (602 req/s) | Spring MVC (428 req/s) |
| Spike | Rust + Axum (sqlx) (2.772 req/s) | Go + Gin (GORM) (1.990 req/s) | Node Fastify (1.692 req/s) | Spring WebFlux (1.244 req/s) | Spring MVC (652 req/s) | FastAPI Async (SQLAlchemy) (586 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-4gb.
- Todas as stacks com **0% de erro** em steady state.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (7.541 req/s), menor p95 = **Rust + Axum (sqlx)** (44,88 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (7.674 req/s), menor p95 = **Rust + Axum (sqlx)** (87,96 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (2.772 req/s), menor p95 = **Rust + Axum (sqlx)** (54,38 ms)