# Resultados v2 — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (Node Fastify: pool dividido entre workers).
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM — testando impacto de mais RAM.
>
> **Stacks testadas:** Rust + Axum (sqlx), Go + Gin (GORM), Node Fastify (cluster mode)

---

## Configuração dos Testes

| Parâmetro | Valor |
|---|---|
| Ferramenta | k6 — 3 cenários por config de hardware |
| Banco de dados | PostgreSQL 16 (Docker) |
| Dataset | 10.000 usuários (9.000 ativos) |
| Endpoints | `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search` |
| Cenários | Steady State (200 VUs, 30s), Ramp-up (0→500 VUs, 80s), Spike (50→500→50 VUs, 75s) |
| Configs | 1 CPU/4GB, 2 CPUs/8GB |

---

## Ranking (2 CPUs / 8GB, Ramp-up)

| # | Stack | Throughput | p95 | Máxima | Erros | Escalabilidade |
|---|---|---|---|---|---|---|
| 1 | **Rust + Axum (sqlx)** | **12.932 req/s** | **50,2 ms** | **78 ms** | **0,37%** | **1.7x** |
| 2 | Go + Gin (GORM) | 8.519 req/s | 104,4 ms | 1.028 ms | 0,11% | 2.0x |
| 3 | Node Fastify | 6.096 req/s | 87,5 ms | 1.740 ms | 0,01% | 1.9x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.**

### 1 CPU / 4GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput | **7.562** | 4.220 | 3.335 |
| p95 | **44,46 ms** | 165,85 ms | 97,46 ms |
| Erros | **0,00%** | **0,00%** | **0,00%** |

### 2 CPU / 8GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| Throughput | **12.921** | 8.574 | 6.321 |
| p95 | **25,06 ms** | 74,23 ms | 61,51 ms |
| Erros | **0,00%** | **0,00%** | **0,00%** |


---

## 2. Ramp-up

**0 → 500 VUs em ~80 segundos.**

| Config | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| 1 CPU | **7.753/s (85,8ms)** | 4.199/s (206,5ms) | 3.284/s (89,3ms) |
| 2 CPU | **12.932/s (50,2ms)** | 8.519/s (104,4ms) | 6.096/s (87,5ms) |

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.**

| Config | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify |
|---|---|---|---|
| 1 CPU | **2.789/s (51,4ms, 0%)** | 1.996/s (190,8ms, 0%) | 1.692/s (71,9ms, 0%) |
| 2 CPU | **3.731/s (10,2ms, 0%)** | 2.912/s (59,6ms, 0%) | 2.253/s (60,7ms, 0%) |

---

## Escalabilidade

| Stack | 1 CPU | 2 CPUs | Escalab. |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.753 | 12.932 | **1.7x** |
| Go + Gin (GORM) | 4.199 | 8.519 | **2.0x** |
| Node Fastify | 3.284 | 6.096 | **1.9x** |

---

## Comparação v1 vs v2

v1 com 1GB/2GB RAM vs v2 com 4GB/8GB RAM — nenhuma diferença significativa.

| Stack | 1 CPU (v2 vs v1) | 2 CPUs (v2 vs v1) |
|---|---|---|
| Rust + Axum (sqlx) | 7.753 vs 7.709 (+0.6%) | 12.932 vs 13.375 (-3.3%) |
| Go + Gin (GORM) | 4.199 vs 4.246 (-1.1%) | 8.519 vs 8.668 (-1.7%) |
| Node Fastify | 3.284 vs 3.144 (+4.5%) | 6.096 vs 5.994 (+1.7%) |

---

## Conclusão

A v2 confirma: **RAM não é gargalo** para nenhuma destas stacks. Os resultados são idênticos aos da v1 com 1/4 da memória.