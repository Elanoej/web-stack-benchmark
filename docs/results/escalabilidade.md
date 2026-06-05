# Benchmarks — Curva de escalabilidade

> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.
> Todas as stacks limitadas a CPU e RAM via Docker. FastAPI com WORKERS = CPUs + 1.

## Throughput (req/s)

| Cenário | Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|---|------|---|---|---|---|
| Steady State (200 VUs) | spring-mvc | 6354 | 379 | 2049 | 3549 | 3838 |
| Steady State (200 VUs) | spring-webflux | 2901 | 606 | 2016 | 4342 | 5958 |
| Steady State (200 VUs) | fastapi-async | 1223 | 1023 | 1579 | 1590 | 1592 |

| Ramp-up (0→500 VUs) | spring-mvc | 408 | 1142 | 3079 | 2875 | 2876 |
| Ramp-up (0→500 VUs) | spring-webflux | 502 | 1894 | 4400 | 7411 | 8852 |
| Ramp-up (0→500 VUs) | fastapi-async | 525 | 1044 | 1599 | 1615 | 1615 |

| Spike (pico 500 VUs) | spring-mvc | 680 | 1369 | 1650 | 1576 | 1596 |
| Spike (pico 500 VUs) | spring-webflux | 1080 | 1621 | 2058 | 2712 | 2972 |
| Spike (pico 500 VUs) | fastapi-async | 467 | 896 | 1192 | 1079 | 1129 |

## Latência p95 (ms)

| Cenário | Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|---|------|---|---|---|---|
| Steady State (200 VUs) | spring-mvc | 23 | 1989 | 300 | 218 | 211 |
| Steady State (200 VUs) | spring-webflux | 24 | 988 | 209 | 103 | 73 |
| Steady State (200 VUs) | fastapi-async | 815 | 504 | 345 | 288 | 286 |

| Ramp-up (0→500 VUs) | spring-mvc | 1514 | 571 | 186 | 209 | 211 |
| Ramp-up (0→500 VUs) | spring-webflux | 1195 | 272 | 152 | 90 | 75 |
| Ramp-up (0→500 VUs) | fastapi-async | 1371 | 680 | 453 | 455 | 463 |

| Spike (pico 500 VUs) | spring-mvc | 886 | 214 | 171 | 192 | 185 |
| Spike (pico 500 VUs) | spring-webflux | 684 | 227 | 121 | 53 | 39 |
| Spike (pico 500 VUs) | fastapi-async | 1480 | 692 | 442 | 455 | 445 |

## Taxa de Erro (%)

| Cenário | Stack | 1 CPU / 1GB | 2 CPUs / 2GB | 4 CPUs / 4GB | 8 CPUs / 8GB | 12 CPUs / 12GB |
|---|------|---|---|---|---|
| Steady State (200 VUs) | spring-mvc | 99.80% | 0.00% | 0.00% | 49.00% | 50.71% |
| Steady State (200 VUs) | spring-webflux | 97.26% | 0.00% | 13.91% | 6.54% | 6.11% |
| Steady State (200 VUs) | fastapi-async | 65.08% | 0.00% | 0.00% | 0.00% | 0.00% |

| Ramp-up (0→500 VUs) | spring-mvc | 0.00% | 0.03% | 0.01% | 0.01% | 0.01% |
| Ramp-up (0→500 VUs) | spring-webflux | 0.00% | 0.00% | 0.01% | 0.08% | 0.16% |
| Ramp-up (0→500 VUs) | fastapi-async | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

| Spike (pico 500 VUs) | spring-mvc | 0.41% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spike (pico 500 VUs) | spring-webflux | 0.17% | 0.00% | 0.00% | 0.00% | 0.00% |
| Spike (pico 500 VUs) | fastapi-async | 0.13% | 0.01% | 0.00% | 0.00% | 0.00% |

## Análise

### Steady State — Erros em todas as configs

O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Com excessão do FastAPI, todas as stacks apresentam erros mesmo com 12 CPUs. Isso ocorre porque:
- **Spring MVC** (thread-per-request): 200 conexões simultâneas exigem 200 threads do pool. Com CPU limitada, threads competem e o backlog de conexões estoura no nginx
- **Spring WebFlux** (reativo): melhora progressivamente com mais CPUs, mas ainda tem ~5% de erro em 12 CPUs — o overhead do R2DBC + reactive streams sob pressão constante
- **FastAPI Async**: **0% de erro a partir de 4 CPUs** — o modelo async I/O + workers = CPUs+1 absorve 200 conexões sem saturar o event loop

### Ramp-up e Spike — Todas as stacks estáveis

Nestes cenários (carga variável com picos), todas as stacks têm erro < 1% em todas as configs a partir de 1 CPU. O modelo gradual permite que o backpressure funcione corretamente em todas as stacks.

### Curva de escalabilidade

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |
|---|---|---|---|---|---|---|
| spring-mvc | 408 | 1142 | 3079 | 2875 | 2876 | 7.1x |
| spring-webflux | 502 | 1894 | 4400 | 7411 | 8852 | 17.6x |
| fastapi-async | 525 | 1044 | 1599 | 1615 | 1615 | 3.1x |

### Observações finais

1. **Spring MVC** escala linearmente até ~4 CPUs e então estabiliza — o throughput não melhora significativamente de 8 para 12 CPUs, indicando que o bottleneck muda para o banco de dados ou nginx
2. **Spring WebFlux** escala melhor que MVC em todos os cenários, com latências significativamente mais baixas. É a stack que mais se beneficia de mais CPUs no ramp-up e spike
3. **FastAPI Async** atinge platô cedo (~4 CPUs, ~1.600 req/s) e não escala além disso — o overhead do ORM (SQLAlchemy + Pydantic) e do GIL dentro de cada worker limita o throughput máximo. Porém, é a única stack com **0% de erro em steady state** a partir de 4 CPUs
4. A **taxa de erro em steady state** é o indicador mais revelador: FastAPI atinge 0% em 4 CPUs, WebFlux precisa de mais recursos para chegar perto, e MVC mantém ~50% de erro mesmo com 12 CPUs — o modelo thread-per-request simplesmente não foi feito para 200 conexões simultâneas com CPU limitada
