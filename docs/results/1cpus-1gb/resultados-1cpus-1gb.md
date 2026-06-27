# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, demais stacks atualizadas para 30). FastAPI com 1 workers. PostgreSQL max_connections=30. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 7656.9 | 3296 | 4249.0 | 175 | 143 | 604.2 |
| Latência média (ms) | 26.02 | 60 | 46.86 | 1134.42 | 1365.90 | 328.32 |
| Latência p50 (ms) | 35.74 | 51 | 21.31 | 1000.45 | 400.89 | 488.96 |
| Latência p90 (ms) | 41.7 | 90 | 107.37 | 2588.86 | 4196.21 | 501.33 |
| Latência p95 (ms) | 44.01 | 101 | 164.69 | 3206.81 | 5300.22 | 531.48 |
| Latência máxima (ms) | 58 | 3960 | 506 | 6587 | 13695 | 1516 |
| Total requisições | 230082 | 99291 | 127887 | 5400 | 4527 | 18468 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 7709.4 | 3112 | 4246.5 | 579 | 400 | 592.7 |
| Latência média (ms) | 27.9 | 72 | 50.8 | 378.09 | 553.97 | 371.28 |
| Latência p50 (ms) | 15.82 | 42 | 12.11 | 295.18 | 392.84 | 145.56 |
| Latência p90 (ms) | 77.91 | 88 | 127.6 | 983.79 | 1302.36 | 1087.87 |
| Latência p95 (ms) | 88.72 | 100 | 204.75 | 1087.00 | 1795.53 | 1234.78 |
| Latência máxima (ms) | 120 | 8926 | 2598 | 1402 | 6006 | 6241 |
| Total requisições | 616764 | 248940 | 339729 | 46347 | 32013 | 47415 |
| Erros | 0,01% | 0.002% | 0,03% | 0,00% | 0,00% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 2764.4 | 1679 | 1983.0 | 1130 | 661 | 578.3 |
| Latência média (ms) | 15.51 | 49 | 34.89 | 87.84 | 177.45 | 209.32 |
| Latência p50 (ms) | 1.91 | 1.6 | 1.36 | 1.92 | 85.93 | 6.96 |
| Latência p90 (ms) | 47.97 | 59 | 108.15 | 511.07 | 501.59 | 1022.16 |
| Latência p95 (ms) | 52.42 | 72 | 193.39 | 600.88 | 892.89 | 1220.68 |
| Latência máxima (ms) | 72 | 6824 | 1286 | 799 | 3905 | 8541 |
| Total requisições | 207471 | 126054 | 148899 | 84873 | 49590 | 43401 |
| Erros | 0,00% | 0,00% | 0,00% | 0,01% | 0,76% | 0,04% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7656.9 req/s) | Node Fastify (3296 req/s) | Go + Gin (GORM) (4249.0 req/s) | FastAPI Async (SQLAlchemy) (604.2 req/s) | Spring WebFlux (147 req/s) | Spring MVC (144 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7656.9 req/s) | Go + Gin (GORM) (4249.0 req/s) | Node Fastify (3112 req/s) | Spring WebFlux (579 req/s) | FastAPI Async (SQLAlchemy) (592.7 req/s) | Spring MVC (400 req/s) |
| Spike | Rust + Axum (sqlx) (7656.9 req/s) | Go + Gin (GORM) (4249.0 req/s) | Node Fastify (1679 req/s) | Spring WebFlux (1130 req/s) | Spring MVC (661 req/s) | FastAPI Async (SQLAlchemy) (578.3 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em Steady State (3296 req/s) e terceiro em Ramp-up (3112 req/s) e Spike (1679 req/s).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (4102 req/s), menor p95 = **Rust + Axum (sqlx)** (84.96 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7032 req/s), menor p95 = **Rust + Axum (sqlx)** (94.05 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2645 req/s), menor p95 = **Rust + Axum (sqlx)** (63.21 ms)
