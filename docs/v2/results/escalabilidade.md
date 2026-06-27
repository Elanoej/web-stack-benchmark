# Benchmarks v2 — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.
> **Diferencial da v2:** 1 CPU / 4GB RAM e 2 CPUs / 8GB RAM (vs 1GB/2GB na v1) — testando se mais RAM faz diferença.

## Throughput (req/s)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.753 | 12.932 |
| Go + Gin (GORM) | 4.199 | 8.519 |
| Node Fastify | 3.284 | 6.096 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.562 | 12.921 |
| Go + Gin (GORM) | 4.220 | 8.574 |
| Node Fastify | 3.335 | 6.321 |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 7.753 | 12.932 |
| Go + Gin (GORM) | 4.199 | 8.519 |
| Node Fastify | 3.284 | 6.096 |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 2.789 | 3.731 |
| Go + Gin (GORM) | 1.996 | 2.912 |
| Node Fastify | 1.692 | 2.253 |

## Latência p95 (ms)

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 85,85 | 50,25 |
| Go + Gin (GORM) | 206,50 | 104,35 |
| Node Fastify | 89,28 | 87,54 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,00% |

**Ramp-up:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,02% | 0,37% |
| Go + Gin (GORM) | 0,04% | 0,11% |
| Node Fastify | 0,00% | 0,01% |

**Spike:**

| Stack | 1 CPU / 4GB | 2 CPUs / 8GB |
|---|---|---|
| Rust + Axum (sqlx) | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,00% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | Escalabilidade |
|---|---|---|---|
| Rust + Axum (sqlx) | 7.753 | 12.932 | 1.7x |
| Go + Gin (GORM) | 4.199 | 8.519 | 2.0x |
| Node Fastify | 3.284 | 6.096 | 1.9x |

## Comparação v2 vs v1

| Stack | Config | v2 (mais RAM) | v1 (menos RAM) | Δ |
|---|---|---|---|---|
| Rust + Axum (sqlx) | 1 CPU | 7.753 req/s | 7.709 req/s | +0.6% |
| Rust + Axum (sqlx) | 2 CPU | 12.932 req/s | 13.375 req/s | -3.3% |
| Go + Gin (GORM) | 1 CPU | 4.199 req/s | 4.246 req/s | -1.1% |
| Go + Gin (GORM) | 2 CPU | 8.519 req/s | 8.668 req/s | -1.7% |
| Node Fastify | 1 CPU | 3.284 req/s | 3.144 req/s | +4.5% |
| Node Fastify | 2 CPU | 6.096 req/s | 5.994 req/s | +1.7% |

## Conclusão da v2

A v2 confirmou que **mais RAM não melhora throughput** para estas stacks. Os resultados são praticamente idênticos aos da v1 com 1GB/2GB.

- **Rust + Axum**: ~7.700 req/s (1 CPU) e ~12.900 req/s (2 CPUs) — mesmo desempenho (±3%)
- **Go + Gin (GORM)**: ~4.200 req/s (1 CPU) e ~8.500 req/s (2 CPUs) — mesmo desempenho (±2%)
- **Node Fastify**: ~3.300 req/s (1 CPU) e ~6.100 req/s (2 CPUs) — mesmo desempenho (±5%)
- **0% de erro** em steady state e spike para todas as stacks

O gargalo continua sendo **CPU**, não memória. As stacks já operam folgadas com 1GB/2GB.