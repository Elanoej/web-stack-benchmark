# Resultados v2 — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30).
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM — testando impacto de mais RAM.
>
> **Stacks testadas:** Rust + Axum (sqlx), Node Fastify (cluster mode), Go + Gin (GORM), Kotlin Ktor (Exposed), Spring WebFlux (Kotlin, R2DBC), Spring MVC (Kotlin, JDBC), FastAPI Async (Python, SQLAlchemy)

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
| 1 | **Rust + Axum (sqlx)** | **12.825 req/s** | **52,2 ms** | **70 ms** | **0,000%** | **1.7x** |
| 2 | Go + Gin (GORM) | 8.674 req/s | 102,4 ms | 741 ms | 0,000% | 2.0x |
| 3 | Node Fastify | 6.139 req/s | 92,1 ms | 228 ms | 0,000% | 1.8x |
| 4 | Kotlin Ktor (Exposed) | 5.005 req/s | 93,3 ms | 121 ms | 0,000% | 1.9x |
| 5 | Spring WebFlux | 2.580 req/s | 212,6 ms | 383 ms | 0,000% | 4.0x |
| 6 | Spring MVC | 1.086 req/s | 704,3 ms | 3.803 ms | 0,000% | 2.6x |
| 7 | FastAPI Async (SQLAlchemy) | 598 req/s | 1.203,2 ms | 4.822 ms | 0,000% | 1.0x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.**

### 1 CPU / 4GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput | **7.709** | 4.329 | 3.513 | 1.222 | 195 | 92 | 609 |
| p95 | **43,83 ms** | 160,85 ms | 96,78 ms | 408,66 ms | 2.701,02 ms | 14.225,93 ms | 904,88 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

### 2 CPU / 8GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| Throughput | **12.969** | 8.735 | 6.464 | 3.343 | 752 | 242 | 601 |
| p95 | **24,67 ms** | 73,37 ms | 57,39 ms | 119,39 ms | 700,06 ms | 2.695,77 ms | 537,35 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |


---

## 2. Ramp-up

**0 → 500 VUs em ~80 segundos.**

| Config | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| 1 CPU | **7.633/s (87,0ms)** | 4.264/s (204,7ms) | 3.375/s (158,8ms) | 2.636/s (175,1ms) | 646/s (804,2ms) | 420/s (1.798,7ms) | 588/s (1.261,0ms) |
| 2 CPU | **12.825/s (52,2ms)** | 8.674/s (102,4ms) | 6.139/s (92,1ms) | 5.005/s (93,3ms) | 2.580/s (212,6ms) | 1.086/s (704,3ms) | 598/s (1.203,2ms) |

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.**

| Config | Rust + Axum (sqlx) | Go + Gin (GORM) | Node Fastify | Kotlin Ktor (Exposed) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|---|
| 1 CPU | **2.750/s (56,8ms, 0%)** | 1.995/s (191,8ms, 0%) | 1.727/s (105,7ms, 0%) | 1.632/s (161,3ms, 0%) | 1.244/s (485,3ms, 0%) | 681/s (796,0ms, 0%) | 579/s (1.226,8ms, 0%) |
| 2 CPU | **3.684/s (11,9ms, 0%)** | 2.952/s (56,4ms, 0%) | 2.324/s (75,1ms, 0%) | 2.203/s (72,4ms, 0%) | 1.732/s (192,4ms, 0%) | 1.807/s (200,3ms, 0%) | 579/s (1.212,5ms, 0%) |

---

## Escalabilidade

| Stack | 1 CPU | 2 CPUs | Escalab. |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 | **1.7x** |
| Go + Gin (GORM) | 4.264 | 8.674 | **2.0x** |
| Node Fastify | 3.375 | 6.139 | **1.8x** |
| Kotlin Ktor (Exposed) | 2.636 | 5.005 | **1.9x** |
| Spring WebFlux | 646 | 2.580 | **4.0x** |
| Spring MVC | 420 | 1.086 | **2.6x** |
| FastAPI Async (SQLAlchemy) | 588 | 598 | **1.0x** |

---

## Comparação v1 vs v2

v1 com 1GB/2GB RAM vs v2 com 4GB/8GB RAM.

| Stack | 1 CPU (v2 vs v1) | 2 CPUs (v2 vs v1) |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 vs 7.709 (-1,0%) | 12.825 vs 13.375 (-4,1%) |
| Go + Gin (GORM) | 4.264 vs 4.246 (+0,4%) | 8.674 vs 8.668 (+0,1%) |
| Node Fastify | 3.375 vs 3.144 (+7,3%) | 6.139 vs 5.994 (+2,4%) |
| Kotlin Ktor (Exposed) | 2.636 vs — (não testado na v1) | 5.005 vs — (não testado na v1) |
| Spring WebFlux | 646 vs 587,1 (+10,0%) | 2.580 vs 2.396 (+7,7%) |
| Spring MVC | 420 vs 405,6 (+3,6%) | 1.086 vs 994,2 (+9,2%) |
| FastAPI Async (SQLAlchemy) | 588 vs 592,7 (-0,8%) | 598 vs 1.189 (-49,7%) |

---

## Conclusão

A v2 trouxe o **Kotlin Ktor** como nova stack, que estreia em **4º lugar geral** — superando todas as stacks JVM tradicionais.

### Ranking Final v2 (2 CPUs / 8GB, Ramp-up)

1. **Rust + Axum (sqlx)**: 12.825 req/s, p95 52,2ms, 0,000% de erro
2. **Go + Gin (GORM)**: 8.674 req/s, p95 102,4ms, 0,000% de erro
3. **Node Fastify**: 6.139 req/s, p95 92,1ms, 0,000% de erro
4. **Kotlin Ktor (Exposed)**: 5.005 req/s, p95 93,3ms, 0,000% de erro
5. **Spring WebFlux**: 2.580 req/s, p95 212,6ms, 0,000% de erro
6. **Spring MVC**: 1.086 req/s, p95 704,3ms, 0,000% de erro
7. **FastAPI Async (SQLAlchemy)**: 598 req/s, p95 1.203,2ms, 0,000% de erro
