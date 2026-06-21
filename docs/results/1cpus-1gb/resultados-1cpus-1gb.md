# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com 2 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 2767 | 4102 | 147 | 113 | 2500 |
| Latência média (ms) | 71.97 | 48.54 | 1340.29 | 1723.13 | 78.67 |
| Latência p50 (ms) | 40.61 | 65.67 | 1305.85 | 696.26 | 16.47 |
| Latência p90 (ms) | 193.60 | 81.59 | 3019.11 | 4501.22 | 86.67 |
| Latência p95 (ms) | 258.55 | 84.96 | 3631.42 | 6996.94 | 492.89 |
| Latência máxima (ms) | 1117 | 130 | 5706 | 10296 | 5686 |
| Total requisições | 83424 | 123576 | 4590 | 3606 | 77376 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 87.21% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 3959 | 7032 | 507 | 432 | 520 |
| Latência média (ms) | 54.50 | 30.59 | 431.41 | 510.49 | 424.50 |
| Latência p50 (ms) | 11.43 | 17.93 | 307.21 | 388.68 | 203.90 |
| Latência p90 (ms) | 164.55 | 84.72 | 1082.34 | 1192.62 | 1180.99 |
| Latência p95 (ms) | 221.16 | 94.05 | 1112.80 | 1496.58 | 1481.05 |
| Latência máxima (ms) | 1733 | 131 | 1385 | 4203 | 8396 |
| Total requisições | 316713 | 562533 | 40605 | 34584 | 41586 |
| Erros | 0.12% | 0.09% | 0,00% | 0,00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 1910 | 2645 | 1135 | 752 | 454 |
| Latência média (ms) | 37.69 | 17.76 | 87.37 | 150.69 | 276.09 |
| Latência p50 (ms) | 1.44 | 1.59 | 1.79 | 17.50 | 79.14 |
| Latência p90 (ms) | 115.51 | 57.30 | 499.79 | 510.30 | 1207.31 |
| Latência p95 (ms) | 203.06 | 63.21 | 614.28 | 712.11 | 1398.12 |
| Latência máxima (ms) | 1267 | 79 | 779 | 3000 | 7190 |
| Total requisições | 143235 | 198378 | 85182 | 56448 | 34071 |
| Erros | 0,00% | 0,00% | 0.20% | 0.83% | 0.22% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (4102 req/s) | Go + Gin (GORM) (2767 req/s) | FastAPI Async (SQLAlchemy) (2500 req/s) | Spring WebFlux (147 req/s) | Spring MVC (113 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7032 req/s) | Go + Gin (GORM) (3959 req/s) | FastAPI Async (SQLAlchemy) (520 req/s) | Spring WebFlux (507 req/s) | Spring MVC (432 req/s) |
| Spike | Rust + Axum (sqlx) (2645 req/s) | Go + Gin (GORM) (1910 req/s) | Spring WebFlux (1135 req/s) | Spring MVC (752 req/s) | FastAPI Async (SQLAlchemy) (454 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-1gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (4102 req/s), menor p95 = **Rust + Axum (sqlx)** (84.96 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (7032 req/s), menor p95 = **Rust + Axum (sqlx)** (94.05 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (2645 req/s), menor p95 = **Rust + Axum (sqlx)** (63.21 ms)
