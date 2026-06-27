# Resultados v2 — 1cpus-4gb

> **Ambiente:** 1 CPUs, 4GB RAM por container. PostgreSQL via Docker. Pool de conexões: 30 por stack (Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 7.562 | 4.220 | 3.335 |
| Latência média (ms) | 26,35 | 47,18 | 59,73 |
| Latência p50 (ms) | 35,93 | 21,50 | 45,94 |
| Latência p90 (ms) | 42,39 | 107,87 | 84,30 |
| Latência p95 (ms) | 44,46 | 165,85 | 97,46 |
| Latência máxima (ms) | 62,48 | 511,10 | 4.272,42 |
| Total requisições | 227.274 | 127.167 | 100.575 |
| Erros | **0,00%** | **0,00%** | **0,00%** |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 7.753 | 4.199 | 3.284 |
| Latência média (ms) | 27,74 | 51,38 | 67,80 |
| Latência p50 (ms) | 16,01 | 12,23 | 39,83 |
| Latência p90 (ms) | 77,06 | 129,17 | 76,10 |
| Latência p95 (ms) | 85,85 | 206,50 | 89,28 |
| Latência máxima (ms) | 112,32 | 1.592,47 | 8.853,43 |
| Total requisições | 620.268 | 335.901 | 262.755 |
| Erros | 0,02% | 0,04% | 0,00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput (req/s) | 2.789 | 1.996 | 1.692 |
| Latência média (ms) | 15,08 | 34,43 | 48,31 |
| Latência p50 (ms) | 1,88 | 1,34 | 1,80 |
| Latência p90 (ms) | 46,96 | 107,96 | 57,12 |
| Latência p95 (ms) | 51,36 | 190,81 | 71,91 |
| Latência máxima (ms) | 71,00 | 1.401,07 | 6.922,02 |
| Total requisições | 209.337 | 149.913 | 127.080 |
| Erros | **0,00%** | **0,00%** | **0,00%** |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º |
|---|---|---|---|
| Steady State | Rust + Axum (sqlx) (7.562 req/s) | Go + Gin (GORM) (4.220 req/s) | Node Fastify (3.335 req/s) |
| Ramp-up | Rust + Axum (sqlx) (7.753 req/s) | Go + Gin (GORM) (4.199 req/s) | Node Fastify (3.284 req/s) |
| Spike | Rust + Axum (sqlx) (2.789 req/s) | Go + Gin (GORM) (1.996 req/s) | Node Fastify (1.692 req/s) |

## Observações

- **Rust + Axum (sqlx)** teve o maior throughput geral em 1cpus-4gb.
- Todas as stacks com **0% de erro** em steady state e spike.
- Em **Steady State**: melhor throughput = **Rust + Axum (sqlx)** (7.562 req/s), menor p95 = **Rust + Axum (sqlx)** (44,46 ms)
- Em **Ramp-up**: melhor throughput = **Rust + Axum (sqlx)** (7.753 req/s), menor p95 = **Rust + Axum (sqlx)** (85,85 ms)
- Em **Spike**: melhor throughput = **Rust + Axum (sqlx)** (2.789 req/s), menor p95 = **Rust + Axum (sqlx)** (51,36 ms)