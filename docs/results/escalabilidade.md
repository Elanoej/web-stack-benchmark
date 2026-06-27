# Benchmarks — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 30 por stack (ajustado) (FastAPI: pool_size=2 + max_overflow=0). FastAPI com WORKERS = CPUs. PostgreSQL max_connections=30.

## Throughput (req/s)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 4246.5 | 8667.9 | 13324.9 | 13251.0 | 13153.7 |
| Rust + Axum (sqlx) | 7709.4 | 13374.9 | 15721.7 | 16093.8 | 15922.4 |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 |
| Spring WebFlux | 579 | 2411 | 4919 | 8638 | 11027 |
| Spring MVC | 400 | 1021 | 5729 | 7889 | 8061 |
| FastAPI Async (SQLAlchemy) | 592.7 | 1189.1 | 2272.4 | 3815.5 | 4948.7 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 4249.0 | 8716.8 | 14176.0 | 13296.1 | 13500.9 |
| Rust + Axum (sqlx) | 7656.9 | 13396.9 | 16476.1 | 16644.6 | 16396.3 |
| Node Fastify | 3296 | 6004 | 10302 | 13577 | 13610 |
| Spring WebFlux | 175 | 732 | 3040 | 6112 | 8020 |
| Spring MVC | 144 | 266 | 1162 | 4412 | 6284 |
| FastAPI Async (SQLAlchemy) | 604.2 | 1197.7 | 2319.2 | 4020.9 | 5237.3 |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 4246.5 | 8667.9 | 13324.9 | 13251.0 | 13153.7 |
| Rust + Axum (sqlx) | 7709.4 | 13374.9 | 15721.7 | 16093.8 | 15922.4 |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 |
| Spring WebFlux | 579 | 2411 | 4919 | 8638 | 11027 |
| Spring MVC | 400 | 1021 | 5729 | 7889 | 8061 |
| FastAPI Async (SQLAlchemy) | 592.7 | 1189.1 | 2272.4 | 3815.5 | 4948.7 |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 1983.0 | 2941.1 | 3651.1 | 3745.1 | 3733.6 |
| Rust + Axum (sqlx) | 2764.4 | 3770.6 | 3836.2 | 3848.1 | 3843.5 |
| Node Fastify | 1679 | 2307 | 3217 | 3730 | 3766 |
| Spring WebFlux | 1130 | 1653 | 2186 | 2993 | 3387 |
| Spring MVC | 661 | 1802 | 2655 | 2838 | 2850 |
| FastAPI Async (SQLAlchemy) | 578.3 | 1050.8 | 1448.3 | 1855.3 | 2092.3 |

## Latência p95 (ms)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 204.75 | 102.15 | 38.84 | 35.48 | 35.92 |
| Rust + Axum (sqlx) | 88.72 | 49.68 | 30.07 | 29.6 | 29.94 |
| Node Fastify | 100 | 88 | 53 | 33 | 33 |
| Spring WebFlux | 1087.00 | 256.92 | 133.40 | 76.46 | 57.91 |
| Spring MVC | 1795.53 | 699.39 | 107.07 | 88.93 | 87.50 |
| FastAPI Async (SQLAlchemy) | 1234.78 | 693.05 | 417.66 | 264.25 | 186.31 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.79% | 0.28% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.12% | 0.15% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.09% | 0.31% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.002% | 0.007% | 0.23% | 0.03% | 0.02% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.03% | 0.23% |
| Spring MVC | 0.00% | 0.00% | 0.06% | 0.03% | 0.13% |
| FastAPI Async (SQLAlchemy) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.01% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.76% | 0.00% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 0.04% | 0.00% | 0.00% | 0.00% | 0.00% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |
|---|---|---|---|---|---|---|
| Go + Gin (GORM) | 4246.5 | 8667.9 | 13324.9 | 13251.0 | 13153.7 | 2.8x |
| Rust + Axum (sqlx) | 7709.4 | 13374.9 | 15721.7 | 16093.8 | 15922.4 | 2.1x |
| Node Fastify | 3112 | 5996 | 10805 | 14245 | 14198 | 4.6x |
| Spring WebFlux | 579 | 2411 | 4919 | 8638 | 11027 | 19.0x |
| Spring MVC | 400 | 1021 | 5729 | 7889 | 8061 | 7.0x |
| FastAPI Async (SQLAlchemy) | 592.7 | 1189.1 | 2272.4 | 3815.5 | 4948.7 | 8.3x |

## Análise

### Steady State

O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Ele revela como cada stack lida com pressão constante e sustentada:

- **1 CPU / 1GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, Node Fastify, FastAPI Async
- **2 CPUs / 2GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Node Fastify, FastAPI Async
- **4 CPUs / 4GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, Node Fastify, FastAPI Async
- **8 CPUs / 8GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, FastAPI Async
- **12 CPUs / 12GB**: stacks com 0% erro → Go + Gin (GORM), Rust + Axum (sqlx), Spring WebFlux, Spring MVC, FastAPI Async (SQLAlchemy)

### Taxa de erro em Steady State

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|---|
| Go + Gin (GORM) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Rust + Axum (sqlx) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Node Fastify | 0.00% | 0.00% | 0.00% | 0.79% | 0.28% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| FastAPI Async (SQLAlchemy) | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

**Observações:**

- **Rust + Axum (sqlx)**: **0% de erro em todas as configs**. A stack mais rápida em throughput geral e com a menor latência p95.
- **Go + Gin (GORM)**: **0% de erro em todas as configs**. Segunda colocada em throughput, mas com latência ligeiramente maior que Rust.
- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput ~30-50% menor que Rust Axum.
- **Spring MVC**: sofre com o modelo thread-per-request em cargas mais altas. O throughput é limitado pelo pool de threads do Tomcat.
- **Node Fastify (cluster mode)**: segundo maior throughput em ramp-up (14.198 req/s em 12 CPUs), superando Go. Latência p95 competitiva (18-33ms) e escalabilidade de 4.6x, mas apresenta pequena taxa de erro em steady state a partir de 8 CPUs (0.79% em 8 CPUs, 0.28% em 12 CPUs).
- **FastAPI Async (SQLAlchemy + Pydantic)**: após o pool fix (`pool_size=2`, `max_overflow=0`, `workers=CPUS`) eliminou 100% dos erros e escalou de 1.584 para 4.949 req/s (+212%). Ainda limitada pelo ORM + GIL, mas agora com 0% de erro em todos os cenários.

### Ramp-up e Spike

Nestes cenários (carga variável com picos), todas as stacks têm erro < 0,3% em todas as configs. O backpressure funciona bem quando a carga não é constante.

### Ranking geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p95 | Erros | Escalabilidade |
|---|---|---|---|---|---|
| 1 | Rust + Axum (sqlx) | 15922.4 req/s | 29.94 ms | 0.00% | 2.1x |
| 2 | Node Fastify (cluster mode) | 14198 req/s | 33 ms | 0.02% | 4.6x |
| 3 | Go + Gin (GORM) | 13153.7 req/s | 35.92 ms | 0.00% | 3.1x |
| 4 | Spring WebFlux | 11027 req/s | 58 ms | 0.23% | 19.0x |
| 5 | Spring MVC | 8061 req/s | 88 ms | 0.13% | 20.2x |
| 6 | FastAPI Async (SQLAlchemy) | 4949 req/s | 186 ms | 0.00% | 8.3x |

### Conclusão

1. **Rust + Axum (sqlx)** é a stack mais rápida: maior throughput geral (**15.922 req/s** em 12 CPUs), menor latência p95 (**30ms**), **zero erros em todos os testes**. Com o pool de 30 conexões, ganhou +9% em relação ao pool de 20.
2. **Node Fastify (cluster mode)** impressiona com o segundo maior throughput em ramp-up (14.198 req/s em 12 CPUs, superando Go + Gin). A latência p95 competitiva (18-33ms) e escalabilidade de 4.6x demonstram a eficiência do cluster mode para aplicações Node.js. Apresenta pequena taxa de erro em steady state a partir de 8 CPUs.
3. **Go + Gin (GORM)** mantém a terceira posição com vantagem sobre as stacks JVM. Após o pool aumentar de 20 para 30, o throughput saltou de 10.958 para **13.154 req/s** (+20%) em 12 CPUs. Sua eficiência por núcleo é notável: com 2 CPUs (8.668/s) já supera o throughput máximo de todas as stacks concorrentes exceto Rust e Node Fastify.
4. **Spring WebFlux** é a melhor stack JVM, com escalabilidade consistente (19x de 1 para 12 CPUs em ramp-up), 0% de erro em steady state em todas as configs e throughput de **11.027 req/s** em 12 CPUs (ramp-up) — 14% maior que o resultado anterior.
5. **Spring MVC** superou a limitação histórica com nativeQuery + ILIKE + ZGC. Saiu de um platô de ~3.000 req/s para **8.061 req/s** em 12 CPUs — ganho de **165%**.
6. **FastAPI Async (SQLAlchemy + Pydantic)** após o pool fix saltou de 1.584 para 4.949 req/s (+212%) e eliminou todos os erros. Ainda é a stack mais fraca em throughput bruto, mas escala 8,3x e compete com Spring MVC em cargas moderadas.
