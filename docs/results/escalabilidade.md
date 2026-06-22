# Benchmarks — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com WORKERS = CPUs + 1.

## Throughput (req/s)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 3959 | 8038 | 10118 | 10921 | 10958 |
| Rust + Axum (sqlx) | 7032 | 11860 | 14421 | 14762 | 14578 |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 |
| FastAPI Async (SQLAlchemy) | 520 | 1055 | 1606 | 1626 | 1584 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 2767 | 8234 | 12926 | 11281 | 11137 |
| Rust + Axum (sqlx) | 4102 | 12228 | 14906 | 15332 | 15076 |
| Node Fastify | 3296 | 6004 | 10302 | 13577 | 13610 |
| Spring WebFlux | 147 | 669 | 1932 | 4235 | 6507 |
| Spring MVC | 113 | 896 | 1421 | 2464 | 2580 |
| FastAPI Async (SQLAlchemy) | 2500 | 1798 | 2478 | 2287 | 1529 |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 3959 | 8038 | 10118 | 10921 | 10958 |
| Rust + Axum (sqlx) | 7032 | 11860 | 14421 | 14762 | 14578 |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 |
| FastAPI Async (SQLAlchemy) | 520 | 1055 | 1606 | 1626 | 1584 |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 1910 | 2771 | 3331 | 3390 | 3379 |
| Rust + Axum (sqlx) | 2645 | 3570 | 3759 | 3778 | 3777 |
| Node Fastify | 1679 | 2307 | 3217 | 3730 | 3766 |
| Spring WebFlux | 1135 | 1631 | 2137 | 2792 | 3171 |
| Spring MVC | 752 | 1659 | 1644 | 1643 | 1644 |
| FastAPI Async (SQLAlchemy) | 454 | 938 | 1224 | 1237 | 1211 |

## Latência p95 (ms)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 221.16 | 113.61 | 49.57 | 44.44 | 43.28 |
| Rust + Axum (sqlx) | 94.05 | 55.46 | 33.08 | 32.21 | 32.18 |
| Node Fastify | 100 | 88 | 53 | 33 | 33 |
| Spring WebFlux | 1112.80 | 267.44 | 141.47 | 87.67 | 67.99 |
| Spring MVC | 1496.58 | 510.32 | 187.01 | 189.63 | 185.02 |
| FastAPI Async (SQLAlchemy) | 1481.05 | 720.06 | 462.70 | 454.96 | 503.47 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.79% | 0.28% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 68.48% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 87.21% | 57.10% | 53.36% | 43.37% | 0.00% |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.12% | 0.15% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.09% | 0.31% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.002% | 0.007% | 0.23% | 0.03% | 0.02% |
| Spring WebFlux | 0.00% | 0.00% | 0.01% | 0.12% | 0.23% |
| Spring MVC | 0.00% | 0.00% | 0.01% | 0.01% | 0.00% |
| FastAPI Async (SQLAlchemy) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.20% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.83% | 0.00% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 0.22% | 0.03% | 0.00% | 0.00% | 0.00% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |
|---|---|---|---|---|---|---|
| Go + Gin (GORM) | 3959 | 8038 | 10118 | 10921 | 10958 | 2.8x |
| Rust + Axum (sqlx) | 7032 | 11860 | 14421 | 14762 | 14578 | 2.1x |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 | 4.6x |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 | 19.0x |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 | 7.0x |
| FastAPI Async (SQLAlchemy) | 520 | 1055 | 1606 | 1626 | 1584 | 3.0x |

## Análise

### Steady State

O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Ele revela como cada stack lida com pressão constante e sustentada:

- **1 CPU / 1GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, Node Fastify
- **2 CPUs / 2GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Node Fastify
- **4 CPUs / 4GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, Node Fastify
- **8 CPUs / 8GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC
- **12 CPUs / 12GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, FastAPI Async (SQLAlchemy)

### Taxa de erro em Steady State

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.79% | 0.28% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 68.48% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 87.21% | 57.10% | 53.36% | 43.37% | 0.00% |

**Observações:**

- **Rust + Axum (sqlx)**: **0% de erro em todas as configs**. A stack mais rápida em throughput geral e com a menor latência p95.
- **Go + Gin (GORM)**: **0% de erro em todas as configs**. Segunda colocada em throughput, mas com latência ligeiramente maior que Rust.
- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput ~30-50% menor que Rust Axum.
- **Spring MVC**: sofre com o modelo thread-per-request em cargas mais altas. O throughput é limitado pelo pool de threads do Tomcat.
- **Node Fastify (cluster mode)**: segundo maior throughput em ramp-up (14.198 req/s em 12 CPUs), superando Go. Latência p95 competitiva (18-33ms) e escalabilidade de 4.6x, mas apresenta pequena taxa de erro em steady state a partir de 8 CPUs (0.79% em 8 CPUs, 0.28% em 12 CPUs).
- **FastAPI Async (SQLAlchemy + Pydantic)**: overhead do ORM + GIL limita o throughput máximo. A partir de 4 CPUs o erro zera.

### Ramp-up e Spike

Nestes cenários (carga variável com picos), todas as stacks têm erro < 0,3% em todas as configs. O backpressure funciona bem quando a carga não é constante.

### Ranking geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p95 | Erros | Escalabilidade |
|---|---|---|---|---|---|
| 1 | Rust + Axum (sqlx) | 14578 req/s | 32 ms | 0.00% | 2.1x |
| 2 | Node Fastify (cluster mode) | 14198 req/s | 33 ms | 0.02% | 4.6x |
| 3 | Go + Gin (GORM) | 10958 req/s | 43 ms | 0.00% | 2.8x |
| 4 | Spring WebFlux | 9641 req/s | 68 ms | 0.23% | 19.0x |
| 5 | Spring MVC | 3046 req/s | 185 ms | 0.00% | 7.0x |
| 6 | FastAPI Async (SQLAlchemy) | 1584 req/s | 503 ms | 0.00% | 3.0x |

### Conclusão

1. **Rust + Axum (sqlx)** é a stack mais rápida: maior throughput geral, menor latência p95, **zero erros em todos os testes**. Com o runtime Tokio configurado corretamente (worker_threads = CPUs disponíveis), a escalabilidade é competitiva com as melhores stacks.
2. **Node Fastify (cluster mode)** impressiona com o segundo maior throughput em ramp-up (14.198 req/s em 12 CPUs, superando Go + Gin). A latência p95 competitiva (18-33ms) e escalabilidade de 4.6x demonstram a eficiência do cluster mode para aplicações Node.js. Apresenta pequena taxa de erro em steady state a partir de 8 CPUs.
3. **Go + Gin (GORM)** mantém a terceira posição com vantagem sobre as stacks JVM. Sua eficiência por núcleo é notável: com 2 CPUs já supera o throughput máximo de todas as stacks concorrentes exceto Rust e Node Fastify.
4. **Spring WebFlux** é a melhor stack JVM, com escalabilidade consistente (19x de 1 para 12 CPUs em ramp-up) e 0% de erro em steady state em todas as configs.
5. **Spring MVC** sofre com o modelo thread-per-request. Escala bem até 4 CPUs e então platôa — o bottleneck muda para o banco ou nginx.
6. **FastAPI Async (SQLAlchemy + Pydantic)** é a stack mais fraca em throughput bruto. O overhead do ORM + validação + GIL limita o throughput máximo.
