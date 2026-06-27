# Resultados v2 — 2cpus-8gb

> **Ambiente:** 2 CPUs, 8GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 12.921 | 8.574 | 6.321 |
| Latência média (ms) | 15,38 | 23,22 | 31,53 |
| Latência p50 (ms) | 21,19 | 15,41 | 28,16 |
| Latência p90 (ms) | 24,19 | 56,47 | 50,36 |
| Latência p95 (ms) | 25,06 | 74,23 | 61,51 |
| Latência máxima (ms) | 66,43 | 358,33 | 1.384,04 |
| Total requisições | 388.002 | 257.607 | 190.029 |
| Erros | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 12.932 | 8.519 | 6.096 |
| Latência média (ms) | 16,58 | 25,24 | 35,33 |
| Latência p50 (ms) | 9,65 | 9,69 | 28,29 |
| Latência p90 (ms) | 45,09 | 68,16 | 73,51 |
| Latência p95 (ms) | 50,25 | 104,35 | 87,54 |
| Latência máxima (ms) | 77,91 | 1.028,45 | 1.740,37 |
| Total requisições | 1.034.556 | 681.504 | 487.713 |
| Erros | 0,37% | 0,11% | 0,01% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 3.731 | 2.912 | 2.253 |
| Latência média (ms) | 2,81 | 13,02 | 26,75 |
| Latência p50 (ms) | 1,30 | 2,10 | 7,96 |
| Latência p90 (ms) | 8,01 | 40,22 | 50,07 |
| Latência p95 (ms) | 10,24 | 59,60 | 60,74 |
| Latência máxima (ms) | 25,72 | 336,11 | 1.672,74 |
| Total requisições | 279.990 | 218.532 | 169.098 |
| Erros | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (12.921 req/s) | Go + Gin (GORM) (8.574 req/s) | Node Fastify (6.321 req/s) |
| Ramp-up | Rust + Axum (sqlx) (12.932 req/s) | Go + Gin (GORM) (8.519 req/s) | Node Fastify (6.096 req/s) |
| Spike | Rust + Axum (sqlx) (3.731 req/s) | Go + Gin (GORM) (2.912 req/s) | Node Fastify (2.253 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 2cpus-8gb.
- Todas as stacks com **0% de erro** em steady state e spike.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (12.921 req/s), menor p95 = **Rust + Axum (sqlx)** (25,06 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (12.932 req/s), menor p95 = **Rust + Axum (sqlx)** (50,25 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (3.731 req/s), menor p95 = **Rust + Axum (sqlx)** (10,24 ms)