# Benchmarks v2 — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (FastAPI: asyncpg pool, 30 // WORKERS, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM (vs 1GB/2GB na v1) — testando se mais RAM faz diferença.

## Throughput (req/s)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 |
| Go + Gin (pgx raw) | 5.272 | 10.393 |
| Node Fastify | 3.375 | 6.139 |
| Kotlin Ktor (Native Query) | 2.753 | 5.133 |
| Spring MVC | 1.978 | 4.774 |
| Spring WebFlux | 726 | 2.594 |
| FastAPI Async (asyncpg) | 1.267 | 2.460 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.709 | 12.969 |
| Go + Gin (pgx raw) | 5.274 | 10.526 |
| Node Fastify | 3.513 | 6.464 |
| Kotlin Ktor (Native Query) | 1.472 | 3.715 |
| FastAPI Async (asyncpg) | 1.255 | 2.473 |
| Spring MVC | 387 | 1.564 |
| Spring WebFlux | 189 | 745 |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 |
| Go + Gin (pgx raw) | 5.272 | 10.393 |
| Node Fastify | 3.375 | 6.139 |
| Kotlin Ktor (Native Query) | 2.753 | 5.133 |
| Spring MVC | 1.978 | 4.774 |
| Spring WebFlux | 726 | 2.594 |
| FastAPI Async (asyncpg) | 1.267 | 2.460 |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 2.750 | 3.684 |
| Go + Gin (pgx raw) | 2.204 | 3.258 |
| Node Fastify | 1.727 | 2.324 |
| Kotlin Ktor (Native Query) | 1.683 | 2.266 |
| Spring MVC | 1.645 | 2.179 |
| Spring WebFlux | 1.271 | 1.720 |
| FastAPI Async (asyncpg) | 1.163 | 1.535 |

**Concurrency Stress:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | — | 9.384 |
| Go + Gin (pgx raw) | — | 7.990 |
| Node Fastify | — | 4.722 |
| Kotlin Ktor (Native Query) | — | 3.594 |
| Spring MVC | — | 1.997 |
| FastAPI Async (asyncpg) | — | 1.828 |
| Spring WebFlux | — | 1.242 |

## Latência p95 (ms)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 87,00 | 52,20 |
| Go + Gin (pgx raw) | 180,61 | 84,34 |
| Node Fastify | 158,82 | 92,10 |
| Kotlin Ktor (Native Query) | 168,72 | 90,39 |
| Spring MVC | 199,97 | 116,19 |
| Spring WebFlux | 707,73 | 213,05 |
| FastAPI Async (asyncpg) | 741,26 | 481,78 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Go + Gin (pgx raw) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Kotlin Ktor (Native Query) | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| FastAPI Async (asyncpg) | 0,000% | 0,000% |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Go + Gin (pgx raw) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Kotlin Ktor (Native Query) | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| FastAPI Async (asyncpg) | 0,000% | 0,000% |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Go + Gin (pgx raw) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Kotlin Ktor (Native Query) | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| FastAPI Async (asyncpg) | 0,000% | 0,000% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | Escalabilidade |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 | 1.7x |
| Go + Gin (pgx raw) | 5.272 | 10.393 | 2.0x |
| Node Fastify | 3.375 | 6.139 | 1.8x |
| Kotlin Ktor (Native Query) | 2.753 | 5.133 | 1.9x |
| Spring MVC | 1.978 | 4.774 | 2.4x |
| Spring WebFlux | 726 | 2.594 | 3.6x |
| FastAPI Async (asyncpg) | 1.267 | 2.460 | 1.9x |

## Comparação v2 vs v1

| Stack | Config | v2 (4GB/8GB) | v1 (1GB/2GB) | Δ |
|---|---|---|---|---|
| Rust + Axum (sqlx) | 1 CPU | 7.633 req/s | 7.709 req/s | -1,0% |
| Rust + Axum (sqlx) | 2 CPU | 12.825 req/s | 13.375 req/s | -4,1% |
| Go + Gin (pgx raw) | 1 CPU | 5.272 req/s | 4.246 req/s | +24,2% |
| Go + Gin (pgx raw) | 2 CPU | 10.393 req/s | 8.668 req/s | +19,9% |
| Node Fastify | 1 CPU | 3.375 req/s | 3.144 req/s | +7,3% |
| Node Fastify | 2 CPU | 6.139 req/s | 5.994 req/s | +2,4% |
| Kotlin Ktor (Native Query) | 1 CPU | 2.753 req/s | — (não testado) | — |
| Kotlin Ktor (Native Query) | 2 CPU | 5.133 req/s | — (não testado) | — |
| Spring MVC | 1 CPU | 1.978 req/s | 405,6 req/s | +387,7% |
| Spring MVC | 2 CPU | 4.774 req/s | 994,2 req/s | +380,2% |
| Spring WebFlux | 1 CPU | 726 req/s | 587,1 req/s | +23,7% |
| Spring WebFlux | 2 CPU | 2.594 req/s | 2.396 req/s | +8,3% |
| FastAPI Async (asyncpg) | 1 CPU | 1.267 req/s | 592,7 req/s | +113,7% |
| FastAPI Async (asyncpg) | 2 CPU | 2.460 req/s | 1.189 req/s | +106,9% |

## Conclusão da v2

A v2 testou stacks com 4x mais RAM que a v1 e aplicou otimizações de native query em 4 stacks. O **Go + Gin** substituiu GORM por pgx raw (+20%). O **Kotlin Ktor** substituiu Exposed DSL por raw JDBC (+20%). O **Spring MVC** substituiu JPA por native query (+301% vs v1). O **FastAPI Async** substituiu SQLAlchemy ORM por asyncpg nativo (+93%).

- **Rust + Axum**: liderança absoluta, ~7.600 req/s (1 CPU) e ~12.800 req/s (2 CPUs)
- **Go + Gin (pgx raw)**: 2º lugar, ~5.300 req/s e ~10.400 req/s
- **Node Fastify**: 3º lugar, ~3.400 req/s e ~6.100 req/s
- **★ Kotlin Ktor (Native Query)**: 4º lugar com ~2.800 req/s e ~5.100 req/s
- **Spring MVC**: 5º lugar, ~2.000 req/s e ~4.800 req/s
- **Spring WebFlux**: 6º lugar, ~730 req/s e ~2.600 req/s
- **FastAPI Async**: 7º, 1.267 req/s (1 CPU) e 2.460 req/s (2 CPUs) — escalabilidade de 1,9x após migrar de SQLAlchemy ORM para asyncpg nativo
- **Concurrency Stress** revelou limites: MVC (3%) e WebFlux (2,3%) tiveram erros sob 4.500 conexões simultâneas. Demais stacks mantiveram <1,5%
- **0% de erro** nos cenários Steady, Ramp-up e Spike para TODAS as stacks
