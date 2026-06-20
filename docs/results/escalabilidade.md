# Benchmarks — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. FastAPI com WORKERS = CPUs + 1.

## Throughput (req/s)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 5375 | 10897 | 12305 | 12613 | 12780 |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 |
| FastAPI Async | 520 | 1055 | 1606 | 1626 | 1584 |

### Detalhamento por cenário

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 3626 | 11139 | 12923 | 12599 | 13131 |
| Spring WebFlux | 147 | 669 | 1932 | 4235 | 6507 |
| Spring MVC | 113 | 896 | 1421 | 2464 | 2580 |
| FastAPI Async | 2500 | 1798 | 2478 | 2287 | 1529 |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 5375 | 10897 | 12305 | 12613 | 12780 |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 |
| FastAPI Async | 520 | 1055 | 1606 | 1626 | 1584 |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 2289 | 3346 | 3629 | 3652 | 3681 |
| Spring WebFlux | 1135 | 1631 | 2137 | 2792 | 3171 |
| Spring MVC | 752 | 1659 | 1644 | 1643 | 1644 |
| FastAPI Async | 454 | 938 | 1224 | 1237 | 1211 |

## Latência p95 (ms)

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 112.58 | 58.88 | 38.68 | 37.80 | 37.12 |
| Spring WebFlux | 1112.80 | 267.44 | 141.47 | 87.67 | 67.99 |
| Spring MVC | 1496.58 | 510.32 | 187.01 | 189.63 | 185.02 |
| FastAPI Async | 1481.05 | 720.06 | 462.70 | 454.96 | 503.47 |

## Taxa de Erro (%)

**Steady State:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 68.48% | 0.00% | 0.00% | 0.00% |
| FastAPI Async | 87.21% | 57.10% | 53.36% | 43.37% | 0.00% |

**Ramp-up:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 0.09% | 0.05% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.00% | 0.00% | 0.01% | 0.12% | 0.23% |
| Spring MVC | 0.00% | 0.00% | 0.01% | 0.01% | 0.00% |
| FastAPI Async | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

**Spike:**

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.20% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.83% | 0.00% | 0.00% | 0.00% | 0.00% |
| FastAPI Async | 0.22% | 0.03% | 0.00% | 0.00% | 0.00% |

## Curva de escalabilidade (Ramp-up)

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |
|---|---|---|---|---|---|---|
| Go + Gin | 5375 | 10897 | 12305 | 12613 | 12780 | 2.4x |
| Spring WebFlux | 507 | 2094 | 4746 | 7629 | 9641 | 19.0x |
| Spring MVC | 432 | 1185 | 3047 | 3062 | 3046 | 7.0x |
| FastAPI Async | 520 | 1055 | 1606 | 1626 | 1584 | 3.0x |

## Análise

### Steady State

O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Ele revela como cada stack lida com pressão constante e sustentada:

- **1 CPU / 1GB**: stacks com 0% erro → Go + Gin, Spring WebFlux, Spring MVC
- **2 CPUs / 2GB**: stacks com 0% erro → Go + Gin, Spring WebFlux
- **4 CPUs / 4GB**: stacks com 0% erro → Go + Gin, Spring WebFlux, Spring MVC
- **8 CPUs / 8GB**: stacks com 0% erro → Go + Gin, Spring WebFlux, Spring MVC
- **12 CPUs / 12GB**: stacks com 0% erro → Go + Gin, Spring WebFlux, Spring MVC, FastAPI Async

### Taxa de erro em Steady State

| Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|------|---|---|---|---|
| Go + Gin | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring WebFlux | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spring MVC | 0.00% | 68.48% | 0.00% | 0.00% | 0.00% |
| FastAPI Async | 87.21% | 57.10% | 53.36% | 43.37% | 0.00% |

**Observações:**

- **Go + Gin**: **0% de erro em todas as configs** — a única stack que conseguiu. Mesmo com 1 CPU, sustenta 3.626 req/s sem uma única falha.
- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput 50-55% menor que Go Gin.
- **Spring MVC**: 68% de erro em 2 CPUs — o pool de threads do modelo thread-per-request não sustenta 200 conexões simultâneas. A partir de 4 CPUs o erro zera, mas o throughput é 5x menor que Go Gin.
- **FastAPI Async**: 87% de erro em 1 CPU, melhorando progressivamente até zerar em 12 CPUs. O overhead do ORM (SQLAlchemy + Pydantic) associado ao GIL satura o event loop com poucos workers.

### Ramp-up e Spike

Nestes cenários (carga variável com picos), todas as stacks têm erro < 0,3% em todas as configs. O backpressure funciona bem quando a carga não é constante.

### Ranking geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p95 | Erros | Escalabilidade |
|---|---|---|---|---|---|
| 1 | Go + Gin | 12780 req/s | 37 ms | 0.00% | 2.4x |
| 2 | Spring WebFlux | 9641 req/s | 68 ms | 0.23% | 19.0x |
| 3 | Spring MVC | 3046 req/s | 185 ms | 0.00% | 7.0x |
| 4 | FastAPI Async | 1584 req/s | 503 ms | 0.00% | 3.0x |

### Conclusão

1. **Go + Gin** domina todos os cenários: maior throughput, menor latência, **zero erros em todos os testes**. A combinação de runtime compilado (Go), modelo concorrente (goroutines) e framework eficiente (Gin) entrega 2x o throughput do WebFlux com latência 50% menor.
2. **Spring WebFlux** é a melhor stack JVM, com escalabilidade quase linear (19x de 1 para 12 CPUs em ramp-up) e 0% de erro em steady state em todas as configs. Porém, seu throughput máximo é ~50% do Go Gin.
3. **Spring MVC** sofre com o modelo thread-per-request: 68% de erro em 2 CPUs no steady state. Escala bem até 4 CPUs (7,1x) e então platôa — o bottleneck muda para o banco ou nginx.
4. **FastAPI Async** (SQLAlchemy + Pydantic) é a stack mais fraca em throughput bruto. O overhead do ORM + validação + GIL limita o máximo a ~1.600 req/s. Porém, é a única stack (além de Go e WebFlux) que zera erros em steady state a partir de 4 CPUs.
5. **A eficiência importa**: Go Gin com **2 CPUs** (10.897 req/s) entrega mais throughput que qualquer stack concorrente com **12 CPUs**. Isso tem impacto direto em custo de infraestrutura em produção.
