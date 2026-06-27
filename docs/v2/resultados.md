# Resultados v2 — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers).
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM — testando impacto de mais RAM.
>
> **Stacks testadas:** Rust + Axum (sqlx), Node Fastify (cluster mode), Go + Gin (GORM), Spring WebFlux (Kotlin, R2DBC), Spring MVC (Kotlin, JDBC), FastAPI Async (Python, SQLAlchemy)

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
| 1 | **Rust + Axum (sqlx)** | **12.885 req/s** | **52,6 ms** | **68 ms** | **0,000%** | **1.7x** |
| 2 | Go + Gin (GORM) | 8.476 req/s | 104,7 ms | 799 ms | 0,000% | 2.0x |
| 3 | Node Fastify | 6.096 req/s | 87,5 ms | 1.740 ms | 0,006% | 1.9x |
| 4 | Spring WebFlux | 2.632 req/s | 212,5 ms | 385 ms | 0,000% | 4.0x |
| 5 | Spring MVC | 954 req/s | 802,7 ms | 3.110 ms | 0,000% | 2.2x |
| 6 | FastAPI Async (SQLAlchemy) | 603 req/s | 1213,1 ms | 4.774 ms | 0,000% | 1.0x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.**

### 1 CPU / 4GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **7.541** | 3.335 | 4.251 | 168,2 | 46,1 | 606,3 |
| p95 | **44,88 ms** | 97,46 ms | 164,50 ms | 3289,20 ms | 20200,18 ms | 965,71 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

### 2 CPU / 8GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **13.152** | 6.321 | 8.504 | 743,3 | 179,2 | 599,5 |
| p95 | **24,47 ms** | 61,51 ms | 75,12 ms | 686,56 ms | 3602,51 ms | 903,92 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |


---

## 2. Ramp-up

**0 → 500 VUs em ~80 segundos.**

| Config | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| 1 CPU | **7.674/s (88,0ms)** | 3.284/s (89,3ms) | 4.172/s (207,5ms) | 650/s (801,6ms) | 428/s (1696,7ms) | 602/s (1201,0ms) |
| 2 CPU | **12.885/s (52,6ms)** | 6.096/s (87,5ms) | 8.476/s (104,7ms) | 2.632/s (212,5ms) | 954/s (802,7ms) | 603/s (1213,1ms) |

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.**

| Config | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| 1 CPU | **2.772/s (54,4ms, 0%)** | 1.692/s (71,9ms, 0%) | 1.990/s (191,9ms, 0%) | 1.244/s (492,4ms, 0%) | 652/s (799,4ms, 0%) | 586/s (1201,0ms, 0%) |
| 2 CPU | **3.698/s (11,1ms, 0%)** | 2.253/s (60,7ms, 0%) | 2.932/s (58,1ms, 0%) | 1.719/s (197,2ms, 0%) | 1.813/s (199,9ms, 0%) | 589/s (1199,5ms, 0%) |

---

## Escalabilidade

| Stack | 1 CPU | 2 CPUs | Escalab. |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.674 | 12.885 | **1.7x** |
| Node Fastify | 3.284 | 6.096 | **1.9x** |
| Go + Gin (GORM) | 4.172 | 8.476 | **2.0x** |
| Spring WebFlux | 650 | 2.632 | **4.0x** |
| Spring MVC | 428 | 954 | **2.2x** |
| FastAPI Async (SQLAlchemy) | 602 | 603 | **1.0x** |

---

## Comparação v1 vs v2

v1 com 1GB/2GB RAM vs v2 com 4GB/8GB RAM.

| Stack | 1 CPU (v2 vs v1) | 2 CPUs (v2 vs v1) |
|---|---|---|
| Rust + Axum (sqlx) | 7.674 vs 7.709 (-0.5%) | 12.885 vs 13.375 (-3.7%) |
| Node Fastify | 3.284 vs 3.144 (+4.5%) | 6.096 vs 5.994 (+1.7%) |
| Go + Gin (GORM) | 4.172 vs 4.246 (-1.8%) | 8.476 vs 8.668 (-2.2%) |
| Spring WebFlux | 650,5 vs 587,1 (+10.8%) | 2.632 vs 2.396 (+9.9%) |
| Spring MVC | 427,7 vs 405,6 (+5.5%) | 953,8 vs 994,2 (-4.1%) |
| FastAPI Async (SQLAlchemy) | 601,8 vs 592,7 (+1.5%) | 602,7 vs 1.189 (-49.3%) |

---

## Conclusão

A v2 confirma que **RAM não é gargalo** para a maioria das stacks — apenas Spring WebFlux teve ganho de ~10% com mais memória, possivelmente beneficiando-se de mais espaço para JIT e GC da JVM.

### Ranking Final v2 (2 CPUs / 8GB, Ramp-up)

1. **Rust + Axum (sqlx)**: 12.885 req/s, p95 52,6ms, 0,000% de erro
2. **Go + Gin (GORM)**: 8.476 req/s, p95 104,7ms, 0,000% de erro
3. **Node Fastify**: 6.096 req/s, p95 87,5ms, 0,006% de erro
4. **Spring WebFlux**: 2.632 req/s, p95 212,5ms, 0,000% de erro
5. **Spring MVC**: 954 req/s, p95 802,7ms, 0,000% de erro
6. **FastAPI Async (SQLAlchemy)**: 603 req/s, p95 1213,1ms, 0,000% de erro