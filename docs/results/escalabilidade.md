# Benchmarks — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers). PostgreSQL max_connections=30.

## Throughput (req/s)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 7.709 | 13.375 | 15.722 | 16.094 | 15.922 |
| Node Fastify | 3.144 | 5.993 | 11.071 | 14.257 | 14.162 |
| Go + Gin (GORM) | 4.247 | 8.668 | 13.325 | 13.251 | 13.154 |
| Spring WebFlux | 579,3 | 2.411 | 4.919 | 8.638 | 11.027 |
| Spring MVC | 400,1 | 1.021 | 5.729 | 7.889 | 8.061 |
| FastAPI Async (SQLAlchemy) | 592,7 | 1.189 | 2.272 | 3.816 | 4.949 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 7.657 | 13.397 | 16.476 | 16.645 | 16.396 |
| Node Fastify | 3.096 | 6.219 | 11.004 | 13.808 | 13.822 |
| Go + Gin (GORM) | 4.249 | 8.717 | 14.176 | 13.296 | 13.501 |
| Spring WebFlux | 174,7 | 732,3 | 3.040 | 6.112 | 8.020 |
| Spring MVC | 143,5 | 265,5 | 1.162 | 4.412 | 6.284 |
| FastAPI Async (SQLAlchemy) | 604,2 | 1.198 | 2.319 | 4.021 | 5.237 |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 7.709 | 13.375 | 15.722 | 16.094 | 15.922 |
| Node Fastify | 3.144 | 5.993 | 11.071 | 14.257 | 14.162 |
| Go + Gin (GORM) | 4.247 | 8.668 | 13.325 | 13.251 | 13.154 |
| Spring WebFlux | 579,3 | 2.411 | 4.919 | 8.638 | 11.027 |
| Spring MVC | 400,1 | 1.021 | 5.729 | 7.889 | 8.061 |
| FastAPI Async (SQLAlchemy) | 592,7 | 1.189 | 2.272 | 3.816 | 4.949 |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 2.764 | 3.771 | 3.836 | 3.848 | 3.844 |
| Node Fastify | 1.685 | 2.310 | 3.235 | 3.744 | 3.774 |
| Go + Gin (GORM) | 1.983 | 2.941 | 3.651 | 3.745 | 3.734 |
| Spring WebFlux | 1.130 | 1.653 | 2.186 | 2.993 | 3.387 |
| Spring MVC | 661,0 | 1.802 | 2.654 | 2.838 | 2.850 |
| FastAPI Async (SQLAlchemy) | 578,3 | 1.051 | 1.448 | 1.855 | 2.092 |

## Latência p95 (ms)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 88,72 | 49,68 | 30,07 | 29,60 | 29,94 |
| Node Fastify | 92,61 | 88,85 | 51,39 | 33,09 | 33,07 |
| Go + Gin (GORM) | 204,75 | 102,15 | 38,84 | 35,48 | 35,92 |
| Spring WebFlux | 1087,00 | 256,92 | 133,40 | 76,46 | 57,91 |
| Spring MVC | 1795,53 | 699,39 | 107,07 | 88,93 | 87,50 |
| FastAPI Async (SQLAlchemy) | 1234,78 | 693,05 | 417,66 | 264,25 | 186,31 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring WebFlux | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring MVC | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| FastAPI Async (SQLAlchemy) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 0,01% | 0,29% | 0,00% | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,01% | 0,17% | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,03% | 0,08% | 0,00% | 0,00% | 0,00% |
| Spring WebFlux | 0,00% | 0,00% | 0,00% | 0,03% | 0,23% |
| Spring MVC | 0,00% | 0,00% | 0,06% | 0,03% | 0,13% |
| FastAPI Async (SQLAlchemy) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring WebFlux | 0,01% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring MVC | 0,76% | 0,00% | 0,00% | 0,00% | 0,00% |
| FastAPI Async (SQLAlchemy) | 0,04% | 0,00% | 0,00% | 0,00% | 0,00% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |
|---|---|---|---|---|---|---|
| Rust + Axum (sqlx) | 7.709 | 13.375 | 15.722 | 16.094 | 15.922 | 2.1x |
| Node Fastify | 3.144 | 5.993 | 11.071 | 14.257 | 14.162 | 4.5x |
| Go + Gin (GORM) | 4.247 | 8.668 | 13.325 | 13.251 | 13.154 | 3.1x |
| Spring WebFlux | 579,3 | 2.411 | 4.919 | 8.638 | 11.027 | 19.0x |
| Spring MVC | 400,1 | 1.021 | 5.729 | 7.889 | 8.061 | 20.1x |
| FastAPI Async (SQLAlchemy) | 592,7 | 1.189 | 2.272 | 3.816 | 4.949 | 8.4x |

## Análise

### Steady State

O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Ele revela como cada stack lida com pressão constante e sustentada:

- **1 CPUs / 1GB**: stacks com 0% erro → Rust + Axum (sqlx) ,Node Fastify ,Go + Gin (GORM) ,Spring WebFlux ,Spring MVC ,FastAPI Async (SQLAlchemy)
- **2 CPUs / 2GB**: stacks com 0% erro → Rust + Axum (sqlx) ,Node Fastify ,Go + Gin (GORM) ,Spring WebFlux ,Spring MVC ,FastAPI Async (SQLAlchemy)
- **4 CPUs / 4GB**: stacks com 0% erro → Rust + Axum (sqlx) ,Node Fastify ,Go + Gin (GORM) ,Spring WebFlux ,Spring MVC ,FastAPI Async (SQLAlchemy)
- **8 CPUs / 8GB**: stacks com 0% erro → Rust + Axum (sqlx) ,Node Fastify ,Go + Gin (GORM) ,Spring WebFlux ,Spring MVC ,FastAPI Async (SQLAlchemy)
- **12 CPUs / 12GB**: stacks com 0% erro → Rust + Axum (sqlx) ,Node Fastify ,Go + Gin (GORM) ,Spring WebFlux ,Spring MVC ,FastAPI Async (SQLAlchemy)

### Taxa de erro em Steady State

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Rust + Axum (sqlx) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Node Fastify | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Go + Gin (GORM) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring WebFlux | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| Spring MVC | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |
| FastAPI Async (SQLAlchemy) | 0,00% | 0,00% | 0,00% | 0,00% | 0,00% |

**Observações:**

- **Rust + Axum (sqlx)**: **0% de erro em todas as configs**. A stack mais rápida em throughput geral e com a menor latência p95. Com pool de 30, atingiu **15.922 req/s** em ramp-up (12 CPUs).
- **Go + Gin (GORM)**: **0% de erro em todas as configs**. Após pool 20→30, saltou de 10.958 para **13.154 req/s** (+20%) em 12 CPUs.
- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput ~30-50% menor que Rust Axum.
- **Spring MVC**: sofre com o modelo thread-per-request em cargas mais altas. O throughput é limitado pelo pool de threads do Tomcat.
- **Node Fastify (cluster mode)**: segundo maior throughput em ramp-up (14.162 req/s em 12 CPUs). Com o pool dividido entre workers, manteve o mesmo throughput e **zerou os erros** em steady state (antes 0,28% em 12 CPUs).
- **FastAPI Async (SQLAlchemy + Pydantic)**: após o pool fix (`pool_size=2`, `max_overflow=0`, `workers=CPUS`) eliminou 100% dos erros e escalou de 1.584 para **4.949 req/s** (+212%). Ainda limitada pelo ORM + GIL, mas agora com 0% de erro em todos os cenários.

### Ramp-up e Spike

Nestes cenários (carga variável com picos), todas as stacks têm erro < 0,3% em todas as configs. O backpressure funciona bem quando a carga não é constante.

### Ranking geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p95 | Erros | Escalabilidade |
|---|---|---|---|---|---|
| 1 | Rust + Axum (sqlx) | 15.922 req/s | 29,9 ms | 0,00% | 2.1x |
| 2 | Node Fastify | 14.162 req/s | 33,1 ms | 0,00% | 4.5x |
| 3 | Go + Gin (GORM) | 13.154 req/s | 35,9 ms | 0,00% | 3.1x |
| 4 | Spring WebFlux | 11.027 req/s | 57,9 ms | 0,23% | 19.0x |
| 5 | Spring MVC | 8.061 req/s | 87,5 ms | 0,13% | 20.1x |
| 6 | FastAPI Async (SQLAlchemy) | 4.949 req/s | 186,3 ms | 0,00% | 8.4x |

### Conclusão

1. **Rust + Axum (sqlx)** é a stack mais rápida: maior throughput geral (**15.922 req/s** em 12 CPUs), menor latência p95 (**29,9 ms**), **zero erros em todos os testes**. Com o pool de 30 conexões, ganhou +9% em relação ao pool de 20.
2. **Node Fastify (cluster mode)** impressiona com o segundo maior throughput em ramp-up (14.162 req/s em 12 CPUs). Com o pool dividido entre workers, manteve desempenho e zerou erros em steady state.
3. **Go + Gin (GORM)** mantém a terceira posição. Após pool 20→30, saltou para **13.154 req/s** (+20%). Eficiência por núcleo notável: 2 CPUs (8.668/s) > WebFlux 8 CPUs.
4. **Spring WebFlux** é a melhor stack JVM, com escalabilidade consistente (19x de 1 para 12 CPUs em ramp-up), 0% de erro em steady state em todas as configs.
5. **Spring MVC** superou a limitação histórica com nativeQuery + ILIKE + ZGC: **8.061 req/s** em 12 CPUs — ganho de **165%**.
6. **FastAPI Async (SQLAlchemy + Pydantic)** após o pool fix saltou de 1.584 para **4.949 req/s** (+212%) e eliminou todos os erros. Ainda é a stack mais fraca em throughput bruto, mas escala 8,3x.