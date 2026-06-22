# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 2 workers. Node Fastify com cluster mode (workers = CPUs).
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 4102 | 3296 | 2767 | 147 | 113 | 2500 |
| Latência média (ms) | 48.54 | 60 | 71.97 | 1340.29 | 1723.13 | 78.67 |
| Latência p50 (ms) | 65.67 | 51 | 40.61 | 1305.85 | 696.26 | 16.47 |
| Latência p90 (ms) | 81.59 | 90 | 193.60 | 3019.11 | 4501.22 | 86.67 |
| Latência p95 (ms) | 84.96 | 101 | 258.55 | 3631.42 | 6996.94 | 492.89 |
| Latência máxima (ms) | 130 | 3960 | 1117 | 5706 | 10296 | 5686 |
| Total requisições | 123576 | 99291 | 83424 | 4590 | 3606 | 77376 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% | 87.21% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 7032 | 3112 | 3959 | 507 | 432 | 520 |
| Latência média (ms) | 30.59 | 72 | 54.50 | 431.41 | 510.49 | 424.50 |
| Latência p50 (ms) | 17.93 | 42 | 11.43 | 307.21 | 388.68 | 203.90 |
| Latência p90 (ms) | 84.72 | 88 | 164.55 | 1082.34 | 1192.62 | 1180.99 |
| Latência p95 (ms) | 94.05 | 100 | 221.16 | 1112.80 | 1496.58 | 1481.05 |
| Latência máxima (ms) | 131 | 8926 | 1733 | 1385 | 4203 | 8396 |
| Total requisições | 562533 | 248940 | 316713 | 40605 | 34584 | 41586 |
| Erros | 0.09% | 0.002% | 0.12% | 0,00% | 0,00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|------|---|---|---|
| Throughput (req/s) | 2645 | 1679 | 1910 | 1135 | 752 | 454 |
| Latência média (ms) | 17.76 | 49 | 37.69 | 87.37 | 150.69 | 276.09 |
| Latência p50 (ms) | 1.59 | 1.6 | 1.44 | 1.79 | 17.50 | 79.14 |
| Latência p90 (ms) | 57.30 | 59 | 115.51 | 499.79 | 510.30 | 1207.31 |
| Latência p95 (ms) | 63.21 | 72 | 203.06 | 614.28 | 712.11 | 1398.12 |
| Latência máxima (ms) | 79 | 6824 | 1267 | 779 | 3000 | 7190 |
| Total requisições | 198378 | 126054 | 143235 | 85182 | 56448 | 34071 |
| Erros | 0,00% | 0,00% | 0,00% | 0.20% | 0.83% | 0.22% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º | 5º | 6º |
|---|---|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (4102 req/s) | Node Fastify (3296 req/s) | Go + Gin (GORM) (2767 req/s) | FastAPI Async (SQLAlchemy) (2500 req/s) | Spring WebFlux (147 req/s) | Spring MVC (113 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7032 req/s) | Go + Gin (GORM) (3959 req/s) | Node Fastify (3112 req/s) | FastAPI Async (SQLAlchemy) (520 req/s) | Spring WebFlux (507 req/s) | Spring MVC (432 req/s) |
| Spike | Rust + Axum (sqlx) (2645 req/s) | Go + Gin (GORM) (1910 req/s) | Node Fastify (1679 req/s) | Spring WebFlux (1135 req/s) | Spring MVC (752 req/s) | FastAPI Async (SQLAlchemy) (454 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- **Node Fastify (cluster mode)** teve o segundo maior throughput em Steady State (3296 req/s) e terceiro em Ramp-up (3112 req/s) e Spike (1679 req/s).
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (4102 req/s), menor p95 = **Rust + Axum (sqlx)** (84.96 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7032 req/s), menor p95 = **Rust + Axum (sqlx)** (94.05 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2645 req/s), menor p95 = **Rust + Axum (sqlx)** (63.21 ms)
