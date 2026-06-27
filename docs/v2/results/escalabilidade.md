# Benchmarks v2 — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM (vs 1GB/2GB na v1) — testando se mais RAM faz diferença.

## Throughput (req/s)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.674 | 12.885 |
| Node Fastify | 3.284 | 6.096 |
| Go + Gin (GORM) | 4.172 | 8.476 |
| Spring WebFlux | 650,5 | 2.632 |
| Spring MVC | 427,7 | 953,8 |
| FastAPI Async (SQLAlchemy) | 601,8 | 602,7 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.541 | 13.152 |
| Node Fastify | 3.335 | 6.321 |
| Go + Gin (GORM) | 4.251 | 8.504 |
| Spring WebFlux | 168,2 | 743,3 |
| Spring MVC | 46,1 | 179,2 |
| FastAPI Async (SQLAlchemy) | 606,3 | 599,5 |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.674 | 12.885 |
| Node Fastify | 3.284 | 6.096 |
| Go + Gin (GORM) | 4.172 | 8.476 |
| Spring WebFlux | 650,5 | 2.632 |
| Spring MVC | 427,7 | 953,8 |
| FastAPI Async (SQLAlchemy) | 601,8 | 602,7 |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 2.772 | 3.698 |
| Node Fastify | 1.692 | 2.253 |
| Go + Gin (GORM) | 1.990 | 2.932 |
| Spring WebFlux | 1.244 | 1.719 |
| Spring MVC | 652,5 | 1.813 |
| FastAPI Async (SQLAlchemy) | 586,3 | 588,7 |

## Latência p95 (ms)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 87,96 | 52,63 |
| Node Fastify | 89,28 | 87,54 |
| Go + Gin (GORM) | 207,46 | 104,70 |
| Spring WebFlux | 801,60 | 212,49 |
| Spring MVC | 1696,73 | 802,70 |
| FastAPI Async (SQLAlchemy) | 1201,02 | 1213,13 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,002% | 0,006% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,000% | 0,000% |
| Node Fastify | 0,000% | 0,000% |
| Go + Gin (GORM) | 0,000% | 0,000% |
| Spring WebFlux | 0,000% | 0,000% |
| Spring MVC | 0,000% | 0,000% |
| FastAPI Async (SQLAlchemy) | 0,000% | 0,000% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | Escalabilidade |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.674 | 12.885 | 1.7x |
| Node Fastify | 3.284 | 6.096 | 1.9x |
| Go + Gin (GORM) | 4.172 | 8.476 | 2.0x |
| Spring WebFlux | 650,5 | 2.632 | 4.0x |
| Spring MVC | 427,7 | 953,8 | 2.2x |
| FastAPI Async (SQLAlchemy) | 601,8 | 602,7 | 1.0x |

## Comparação v2 vs v1

| Stack | Config | v2 (mais RAM) | v1 (menos RAM) | Δ |
|---|---|---|---|---|
| Rust + Axum (sqlx) | 1 CPU | 7.674 req/s | 7.709 req/s | -0.5% |
| Rust + Axum (sqlx) | 2 CPU | 12.885 req/s | 13.375 req/s | -3.7% |
| Node Fastify | 1 CPU | 3.284 req/s | 3.144 req/s | +4.5% |
| Node Fastify | 2 CPU | 6.096 req/s | 5.994 req/s | +1.7% |
| Go + Gin (GORM) | 1 CPU | 4.172 req/s | 4.246 req/s | -1.8% |
| Go + Gin (GORM) | 2 CPU | 8.476 req/s | 8.668 req/s | -2.2% |
| Spring WebFlux | 1 CPU | 650,5 req/s | 587,1 req/s | +10.8% |
| Spring WebFlux | 2 CPU | 2.632 req/s | 2.396 req/s | +9.9% |
| Spring MVC | 1 CPU | 427,7 req/s | 405,6 req/s | +5.5% |
| Spring MVC | 2 CPU | 953,8 req/s | 994,2 req/s | -4.1% |
| FastAPI Async (SQLAlchemy) | 1 CPU | 601,8 req/s | 592,7 req/s | +1.5% |
| FastAPI Async (SQLAlchemy) | 2 CPU | 602,7 req/s | 1.189 req/s | -49.3% |

## Conclusão da v2

A v2 confirmou que **mais RAM não melhora throughput significativamente** para a maioria das stacks. Apenas Spring WebFlux (+10%) se beneficiou de 4x mais memória, provavelmente por mais espaço para JIT e GC.

- **Rust + Axum**: ~7.700 req/s (1 CPU) e ~12.900 req/s (2 CPUs) — mesmo desempenho (±3%)
- **Go + Gin (GORM)**: ~4.200 req/s (1 CPU) e ~8.500 req/s (2 CPUs) — mesmo desempenho (±2%)
- **Node Fastify**: ~3.300 req/s (1 CPU) e ~6.100 req/s (2 CPUs) — mesmo desempenho (±5%)
- **Spring WebFlux**: 650 req/s (1 CPU) e 2.632 req/s (2 CPUs) — **+10%** com mais RAM
- **Spring MVC**: ~430 req/s (1 CPU) e ~950 req/s (2 CPUs) — mesmo desempenho (±5%)
- **FastAPI Async (SQLAlchemy)**: mesmo desempenho da v1
- **0% de erro** em steady state para todas as stacks

O gargalo continua sendo **CPU**, não memória. A exceção é WebFlux, que se beneficia de mais RAM para o JIT da JVM.