# Benchmarks v2 — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers, Ktor: maximumPoolSize=30). PostgreSQL max_connections=30.
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM (vs 1GB/2GB na v1) — testando se mais RAM faz diferença.

## Throughput (req/s)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 |
| Node Fastify | 3.375 | 6.139 |
| Go + Gin (GORM) | 4.264 | 8.674 |
| Kotlin Ktor (Exposed) | 2.636 | 5.005 |
| Spring WebFlux | 646 | 2.580 |
| Spring MVC | 420 | 1.086 |
| FastAPI Async (SQLAlchemy) | 588 | 598 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.709 | 12.969 |
| Node Fastify | 3.513 | 6.464 |
| Go + Gin (GORM) | 4.329 | 8.735 |
| Kotlin Ktor (Exposed) | 1.222 | 3.343 |
| Spring WebFlux | 195 | 752 |
| Spring MVC | 92 | 242 |
| FastAPI Async (SQLAlchemy) | 609 | 601 |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 |
| Node Fastify | 3.375 | 6.139 |
| Go + Gin (GORM) | 4.264 | 8.674 |
| Kotlin Ktor (Exposed) | 2.636 | 5.005 |
| Spring WebFlux | 646 | 2.580 |
| Spring MVC | 420 | 1.086 |
| FastAPI Async (SQLAlchemy) | 588 | 598 |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 2.750 | 3.684 |
| Node Fastify | 1.727 | 2.324 |
| Go + Gin (GORM) | 1.995 | 2.952 |
| Kotlin Ktor (Exposed) | 1.632 | 2.203 |
| Spring WebFlux | 1.244 | 1.732 |
| Spring MVC | 681 | 1.807 |
| FastAPI Async (SQLAlchemy) | 579 | 579 |

## Latência p95 (ms)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 87,00 | 52,20 |
| Node Fastify | 158,82 | 92,10 |
| Go + Gin (GORM) | 204,70 | 102,36 |
| Kotlin Ktor (Exposed) | 175,08 | 93,29 |
| Spring WebFlux | 804,17 | 212,62 |
| Spring MVC | 1.798,73 | 704,26 |
| FastAPI Async (SQLAlchemy) | 1.260,96 | 1.203,16 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Kotlin Ktor (Exposed) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Kotlin Ktor (Exposed) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Kotlin Ktor (Exposed) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | Escalabilidade |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.633 | 12.825 | 1.7x |
| Node Fastify | 3.375 | 6.139 | 1.8x |
| Go + Gin (GORM) | 4.264 | 8.674 | 2.0x |
| Kotlin Ktor (Exposed) | 2.636 | 5.005 | 1.9x |
| Spring WebFlux | 646 | 2.580 | 4.0x |
| Spring MVC | 420 | 1.086 | 2.6x |
| FastAPI Async (SQLAlchemy) | 588 | 598 | 1.0x |

## Comparação v2 vs v1

| Stack | Config | v2 (4GB/8GB) | v1 (1GB/2GB) | Δ |
|---|---|---|---|---|
| Rust + Axum (sqlx) | 1 CPU | 7.633 req/s | 7.709 req/s | -1,0% |
| Rust + Axum (sqlx) | 2 CPU | 12.825 req/s | 13.375 req/s | -4,1% |
| Node Fastify | 1 CPU | 3.375 req/s | 3.144 req/s | +7,3% |
| Node Fastify | 2 CPU | 6.139 req/s | 5.994 req/s | +2,4% |
| Go + Gin (GORM) | 1 CPU | 4.264 req/s | 4.246 req/s | +0,4% |
| Go + Gin (GORM) | 2 CPU | 8.674 req/s | 8.668 req/s | +0,1% |
| Kotlin Ktor (Exposed) | 1 CPU | 2.636 req/s | — (não testado) | — |
| Kotlin Ktor (Exposed) | 2 CPU | 5.005 req/s | — (não testado) | — |
| Spring WebFlux | 1 CPU | 646 req/s | 587,1 req/s | +10,0% |
| Spring WebFlux | 2 CPU | 2.580 req/s | 2.396 req/s | +7,7% |
| Spring MVC | 1 CPU | 420 req/s | 405,6 req/s | +3,6% |
| Spring MVC | 2 CPU | 1.086 req/s | 994,2 req/s | +9,2% |
| FastAPI Async (SQLAlchemy) | 1 CPU | 588 req/s | 592,7 req/s | -0,8% |
| FastAPI Async (SQLAlchemy) | 2 CPU | 598 req/s | 1.189 req/s | -49,7% |

## Conclusão da v2

A v2 testou stacks com 4x mais RAM que a v1. Spring WebFlux e Spring MVC se beneficiaram mais de RAM adicional.
Kotlin Ktor estreia na v2 em **4º lugar geral**, superando todas as stacks JVM tradicionais.

- **Rust + Axum**: liderança absoluta, ~7.600 req/s (1 CPU) e ~12.800 req/s (2 CPUs)
- **Go + Gin**: 2º lugar, ~4.300 req/s e ~8.700 req/s
- **Node Fastify**: 3º lugar, ~3.400 req/s e ~6.100 req/s
- **★ Kotlin Ktor (Exposed)**: estreia em 4º com ~2.600 req/s e ~5.000 req/s — **94% mais rápido que WebFlux**
- **Spring WebFlux**: 5º lugar, beneficiou-se de mais RAM (+10% a +8%)
- **Spring MVC**: 6º lugar, thread-per-request ainda é o gargalo, mas ganhou +9% com RAM extra
- **FastAPI Async**: 7º, limitada pelo GIL + ORM
- **0% de erro** em TODOS os cenários para TODAS as stacks
