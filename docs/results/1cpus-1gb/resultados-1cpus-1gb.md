# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 2 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 4102 | 3296 | 2767 | 175 | 143 | 2500 |
| Latência média (ms) | 48.54 | 60 | 71.97 | 1134.42 | 1365.90 | 78.67 |
| Latência p50 (ms) | 65.67 | 51 | 40.61 | 1000.45 | 400.89 | 16.47 |
| Latência p90 (ms) | 81.59 | 90 | 193.60 | 2588.86 | 4196.21 | 86.67 |
| Latência p95 (ms) | 84.96 | 101 | 258.55 | 3206.81 | 5300.22 | 492.89 |
| Latência máxima (ms) | 130 | 3960 | 1117 | 6587 | 13695 | 5686 |
| Total requisições | 123576 | 99291 | 83424 | 5400 | 4527 | 77376 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 87.21% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 7032 | 3112 | 3959 | 579 | 400 | 520 |
| Latência média (ms) | 30.59 | 72 | 54.50 | 378.09 | 553.97 | 424.50 |
| Latência p50 (ms) | 17.93 | 42 | 11.43 | 295.18 | 392.84 | 203.90 |
| Latência p90 (ms) | 84.72 | 88 | 164.55 | 983.79 | 1302.36 | 1180.99 |
| Latência p95 (ms) | 94.05 | 100 | 221.16 | 1087.00 | 1795.53 | 1481.05 |
| Latência máxima (ms) | 131 | 8926 | 1733 | 1402 | 6006 | 8396 |
| Total requisições | 562533 | 248940 | 316713 | 46347 | 32013 | 41586 |
| Erros | 0.09% | 0.002% | 0.12% | 0,00% | 0,00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 2645 | 1679 | 1910 | 1130 | 661 | 454 |
| Latência média (ms) | 17.76 | 49 | 37.69 | 87.84 | 177.45 | 276.09 |
| Latência p50 (ms) | 1.59 | 1.6 | 1.44 | 1.92 | 85.93 | 79.14 |
| Latência p90 (ms) | 57.30 | 59 | 115.51 | 511.07 | 501.59 | 1207.31 |
| Latência p95 (ms) | 63.21 | 72 | 203.06 | 600.88 | 892.89 | 1398.12 |
| Latência máxima (ms) | 79 | 6824 | 1267 | 799 | 3905 | 7190 |
| Total requisições | 198378 | 126054 | 143235 | 84873 | 49590 | 34071 |
| Erros | 0,00% | 0,00% | 0,00% | 0,01% | 0,76% | 0.22% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (4102 req/s) | Node Fastify (3296 req/s) | Go + Gin (GORM) (2767 req/s) | FastAPI Async (SQLAlchemy) (2500 req/s) | Spring WebFlux (147 req/s) | Spring MVC (144 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7032 req/s) | Go + Gin (GORM) (3959 req/s) | Node Fastify (3112 req/s) | Spring WebFlux (579 req/s) | FastAPI Async (SQLAlchemy) (520 req/s) | Spring MVC (400 req/s) |
| Spike | Rust + Axum (sqlx) (2645 req/s) | Go + Gin (GORM) (1910 req/s) | Node Fastify (1679 req/s) | Spring WebFlux (1130 req/s) | Spring MVC (661 req/s) | FastAPI Async (SQLAlchemy) (454 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em Steady State (3296 req/s) e terceiro em Ramp-up (3112 req/s) e Spike (1679 req/s).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (4102 req/s), menor p95 = **Rust + Axum (sqlx)** (84.96 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7032 req/s), menor p95 = **Rust + Axum (sqlx)** (94.05 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2645 req/s), menor p95 = **Rust + Axum (sqlx)** (63.21 ms)
