# Resultados — 2cpus-2gb

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker. FastAPI com 3 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 8234 | 11965 | 669 | 896 | 1798 |
| Latência média (ms) | 24.18 | 16.62 | 297.73 | 220.82 | 110.10 |
| Latência p50 (ms) | 14.10 | 20.72 | 294.83 | 15.59 | 18.49 |
| Latência p90 (ms) | 62.15 | 25.42 | 590.42 | 694.66 | 330.27 |
| Latência p95 (ms) | 82.67 | 26.73 | 896.03 | 1205.87 | 488.80 |
| Latência máxima (ms) | 373 | 266 | 2685 | 10199 | 3363 |
| Total requisições | 247398 | 359373 | 20319 | 27435 | 54834 |
| Erros | 0,00% | 0,00% | 0,00% | 68.48% | 57.10% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 8038 | 11829 | 2094 | 1185 | 1055 |
| Latência média (ms) | 26.76 | 18.13 | 103.14 | 182.89 | 206.35 |
| Latência p50 (ms) | 9.11 | 9.39 | 102.65 | 132.93 | 101.87 |
| Latência p90 (ms) | 74.22 | 48.45 | 226.60 | 394.50 | 554.22 |
| Latência p95 (ms) | 113.61 | 55.24 | 267.44 | 510.32 | 720.06 |
| Latência máxima (ms) | 1053 | 88 | 362 | 2023 | 4595 |
| Total requisições | 643017 | 946317 | 167520 | 94776 | 84429 |
| Erros | 0.15% | 0.34% | 0,00% | 0.00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Rust + Axum (sqlx) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|---|
| Throughput (req/s) | 2771 | 3521 | 1631 | 1659 | 938 |
| Latência média (ms) | 15.39 | 4.95 | 49.85 | 48.36 | 113.26 |
| Latência p50 (ms) | 2.14 | 2.44 | 1.62 | 10.43 | 9.55 |
| Latência p90 (ms) | 47.53 | 12.73 | 211.60 | 152.88 | 503.99 |
| Latência p95 (ms) | 71.13 | 15.67 | 223.21 | 163.18 | 656.54 |
| Latência máxima (ms) | 529 | 40 | 285 | 575 | 5665 |
| Total requisições | 207966 | 264360 | 122370 | 124470 | 70374 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% | 0.03% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (11965 req/s) | Go + Gin (GORM) (8234 req/s) | FastAPI Async (SQLAlchemy) (1798 req/s) | Spring MVC (896 req/s) | Spring WebFlux (669 req/s) |
| Ramp-up | Rust + Axum (sqlx) (11829 req/s) | Go + Gin (GORM) (8038 req/s) | Spring WebFlux (2094 req/s) | Spring MVC (1185 req/s) | FastAPI Async (SQLAlchemy) (1055 req/s) |
| Spike | Rust + Axum (sqlx) (3521 req/s) | Go + Gin (GORM) (2771 req/s) | Spring MVC (1659 req/s) | Spring WebFlux (1631 req/s) | FastAPI Async (SQLAlchemy) (938 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-2gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Rust + Axum (sqlx)** (11965 req/s), menor p95 = **Rust + Axum (sqlx)** (26.73 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Rust + Axum (sqlx)** (11829 req/s), menor p95 = **Rust + Axum (sqlx)** (55.24 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Rust + Axum (sqlx)** (3521 req/s), menor p95 = **Rust + Axum (sqlx)** (15.67 ms)
