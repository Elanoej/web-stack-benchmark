# Resultados v2 — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (FastAPI: asyncpg pool, 30 // WORKERS, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30).
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM — testando impacto de mais RAM.
>
> **Stacks testadas:** Rust + Axum (sqlx), Node Fastify (cluster mode), Go + Gin (pgx raw), Kotlin Ktor (Native Query), Spring WebFlux (Kotlin, R2DBC), Spring MVC (Kotlin, JDBC), FastAPI Async (Python, asyncpg + Pydantic)

---

## Configuração dos Testes

| Parâmetro | Valor |
|---|---|
| Ferramenta | k6 — 3 cenários por config de hardware |
| Banco de dados | PostgreSQL 16 (Docker) |
| Dataset | 10.000 usuários (9.000 ativos) |
| Endpoints | `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search` |
| Cenários | Steady State (200 VUs, 30s), Ramp-up (0→500 VUs, 80s), Spike (50→500→50 VUs, 75s), Concurrency Stress (0→1500 VUs, 75s, batch 3x) |
| Configs | 1 CPU/4GB, 2 CPUs/8GB |

---

## Ranking (2 CPUs / 8GB, Ramp-up)

| # | Stack | Throughput | p95 | Máxima | Erros | Escalabilidade |
|---|---|---|---|---|---|---|
| 1 | **Rust + Axum (sqlx)** | **12.825 req/s** | **52,2 ms** | **70 ms** | **0,000%** | **1.7x** |
| 2 | Go + Gin (pgx raw) | 10.393 req/s | 84,3 ms | 820 ms | 0,000% | 2.0x |
| 3 | Node Fastify | 6.139 req/s | 92,1 ms | 228 ms | 0,000% | 1.8x |
| 4 | Kotlin Ktor (Native Query) | **5.133 req/s** | **90,4 ms** | **119 ms** | **0,000%** | **1.9x** |
| 5 | Spring MVC | 4.774 req/s | 116,2 ms | 485 ms | 0,000% | 2.4x |
| 6 | Spring WebFlux | 2.594 req/s | 213,1 ms | 384 ms | 0,000% | 3.6x |
| 7 | FastAPI Async (asyncpg) | 2.460 req/s | 481,8 ms | 5.001 ms | 0,000% | 1.9x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.**

### 1 CPU / 4GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (pgx raw) | Node Fastify | Kotlin Ktor (Native Query) | FastAPI Async (asyncpg) | Spring MVC | Spring WebFlux |
|---|---|---|---|---|---|---|---|
| Throughput | **7.709** | 5.274 | 3.513 | **1.472** | 1.255 | 387 | 189 |
| p95 | **43,83 ms** | 111,57 ms | 96,78 ms | **319,78 ms** | 479,57 ms | 1.646,77 ms | 2.998,66 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |

### 2 CPU / 8GB

| Métrica | Rust + Axum (sqlx) | Go + Gin (pgx raw) | Node Fastify | Kotlin Ktor (Native Query) | Spring MVC | Spring WebFlux | FastAPI Async (asyncpg) |
|---|---|---|---|---|---|---|---|
| Throughput | **12.969** | 10.526 | 6.464 | **3.715** | 1.564 | 745 | 2.473 |
| p95 | **24,67 ms** | 60,38 ms | 57,39 ms | **105,08 ms** | 255,53 ms | 700,17 ms | 365,86 ms |
| Erros | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** | **0,000%** |


---

## 2. Ramp-up

**0 → 500 VUs em ~80 segundos.**

| Config | Rust + Axum (sqlx) | Go + Gin (pgx raw) | Node Fastify | Kotlin Ktor (Native Query) | Spring MVC | Spring WebFlux | FastAPI Async (asyncpg) |
|---|---|---|---|---|---|---|---|
| 1 CPU | **7.633/s (87,0ms)** | 5.272/s (180,6ms) | 3.375/s (158,8ms) | **2.753/s (168,7ms)** | 1.978/s (200,0ms) | 726/s (707,7ms) | 1.267/s (741,3ms) |
| 2 CPU | **12.825/s (52,2ms)** | 10.393/s (84,3ms) | 6.139/s (92,1ms) | **5.133/s (90,4ms)** | 4.774/s (116,2ms) | 2.594/s (213,1ms) | 2.460/s (481,8ms) |

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.**

| Config | Rust + Axum (sqlx) | Go + Gin (pgx raw) | Node Fastify | Kotlin Ktor (Native Query) | Spring MVC | Spring WebFlux | FastAPI Async (asyncpg) |
|---|---|---|---|---|---|---|---|
| 1 CPU | **2.750/s (56,8ms, 0%)** | 2.204/s (140,5ms, 0%) | 1.727/s (105,7ms, 0%) | **1.683/s (144,8ms, 0%)** | 1.645/s (190,1ms, 0%) | 1.271/s (485,4ms, 0%) | 1.163/s (552,8ms, 0%) |
| 2 CPU | **3.684/s (11,9ms, 0%)** | 3.258/s (33,2ms, 0%) | 2.324/s (75,1ms, 0%) | **2.266/s (66,9ms, 0%)** | 2.179/s (100,7ms, 0%) | 1.720/s (197,6ms, 0%) | 1.535/s (345,4ms, 0%) |

---

## 4. Concurrency Stress

**0 → 1.500 VUs em 75 segundos, 3 requisições simultâneas por VU via http.batch(). Concorrência efetiva: até 4.500 requisições concorrentes.**

| Stack | Throughput | p95 | Erros |
|---|---|---|---|
| **Rust + Axum (sqlx)** | **9.384 req/s** | **94,8 ms** | **0,33%** |
| Go + Gin (pgx raw) | 7.990 req/s | 168,9 ms | 0,36% |
| Node Fastify | 4.722 req/s | 129,1 ms | 0,81% |
| Kotlin Ktor (Native Query) | 3.594 req/s | 190,9 ms | 0,93% |
| Spring MVC | 1.997 req/s | 617,7 ms | 2,99% |
| FastAPI Async (asyncpg) | 1.828 req/s | 990,3 ms | 1,44% |
| Spring WebFlux | 1.242 req/s | 1.006,6 ms | 2,31% |

O cenário mais agressivo revela como cada stack se comporta sob conexões simultâneas extremas. Rust e Go mantêm degradação controlada (~23-27%). MVC e WebFlux sofrem com thread pool esgotado e overhead reativo. FastAPI com 2 workers + asyncpg raw passa ambos, confirmando que ORM e framework pesado custam mais que o modelo de concorrência.

---

## Escalabilidade

| Stack | 1 CPU | 2 CPUs | Escalab. |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 | **1.7x** |
| Go + Gin (pgx raw) | 5.272 | 10.393 | **2.0x** |
| Node Fastify | 3.375 | 6.139 | **1.8x** |
| Kotlin Ktor (Native Query) | 2.753 | 5.133 | **1.9x** |
| Spring MVC | 1.978 | 4.774 | **2.4x** |
| Spring WebFlux | 726 | 2.594 | **3.6x** |
| FastAPI Async (asyncpg) | 1.267 | 2.460 | **1.9x** |

---

## Comparação v1 vs v2

v1 com 1GB/2GB RAM vs v2 com 4GB/8GB RAM.

| Stack | 1 CPU (v2 vs v1) | 2 CPUs (v2 vs v1) |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 vs 7.709 (-1,0%) | 12.825 vs 13.375 (-4,1%) |
| Go + Gin (pgx raw) | 5.272 vs 4.246 (+24,2%) | 10.393 vs 8.668 (+19,9%) |
| Node Fastify | 3.375 vs 3.144 (+7,3%) | 6.139 vs 5.994 (+2,4%) |
| Kotlin Ktor (Native Query) | 2.753 vs — (não testado na v1) | 5.133 vs — (não testado na v1) |
| Spring MVC | 1.978 vs 405,6 (+387,7%) | 4.774 vs 994,2 (+380,2%) |
| Spring WebFlux | 726 vs 587,1 (+23,7%) | 2.594 vs 2.396 (+8,3%) |
| FastAPI Async (asyncpg) | 1.267 vs 592,7 (+113,7%) | 2.460 vs 1.189 (+106,9%) |

---

## Conclusão

A v2 aplicou otimizações de native query em 4 stacks. O **Go + Gin** substituiu GORM por pgx raw (+20% em ramp-up). O **Kotlin Ktor** substituiu Exposed DSL por raw JDBC (+20%). O **Spring MVC** substituiu JPA por native query (+301% vs v1). O **FastAPI Async** substituiu SQLAlchemy ORM por asyncpg nativo (+93% em ramp-up).

### Ranking Final v2 (2 CPUs / 8GB, Ramp-up)

1. **Rust + Axum (sqlx)**: 12.825 req/s, p95 52,2ms, 0,000% de erro
2. **Go + Gin (pgx raw)**: 10.393 req/s, p95 84,3ms, 0,000% de erro
3. **Node Fastify**: 6.139 req/s, p95 92,1ms, 0,000% de erro
4. **Kotlin Ktor (Native Query)**: 5.133 req/s, p95 90,4ms, 0,000% de erro
5. **Spring MVC**: 4.774 req/s, p95 116,2ms, 0,000% de erro
6. **Spring WebFlux**: 2.594 req/s, p95 213,1ms, 0,000% de erro
7. **FastAPI Async (asyncpg)**: 2.460 req/s, p95 481,8ms, 0,000% de erro
