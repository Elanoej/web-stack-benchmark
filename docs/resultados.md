# Resultados do Benchmark

> Resultados coletados com k6. Mesmo banco de dados, mesmos dados e mesmos scripts.
> Único diferencial é o backend.
>
> **Ambiente:** execução local, PostgreSQL via Docker.

---

## Configuração dos Testes

| Parâmetro | Valor |
|---|---|
| Ferramenta | k6 |
| Banco de dados | PostgreSQL 16 (Docker) |
| Dataset | 10.000 usuários (9.000 ativos) |
| Endpoints testados | `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search` |

---

## 1. Steady State
  
**Configuração:** 200 VUs simultâneos, 30 segundos, sem sleep entre requisições.
  
**Objetivo:** medir throughput sustentado e latência sob pressão constante.
  
| Métrica | Spring MVC | Spring WebFlux | FastAPI Async (raw) | FastAPI Async (ORM) |
|---|---|---|---|---|---|
| Throughput | 2.953 req/s | 2.226 req/s | 1.870 req/s | 1.495 req/s |
| Latência média | 67.49ms | 89.59ms | 181.07ms | 132.57ms |
| Latência mediana (p50) | 89.76ms | 24.40ms | 10.93ms | 83.05ms |
| Latência p90 | 118.79ms | 37.04ms | 108.43ms | 198.33ms |
| Latência p95 | 183.50ms | 46.35ms | 180.87ms | 287.54ms |
| Latência máxima | 614ms | 4.37s | 9.90s | 5.12s |
| Total de requisições | 89.121 | 70.546 | 30.039 | 45.471 |
| Iterações completas | 29.707 | 23.515 | 9.994 | 15.157 |
| Erros | 0 (0.00%) | 0 (0.00%) | 2 (0.01%) | 10.092 (22.19%) |
| Dados recebidos | 268 MB | 198 MB | 84 MB | 85 MB |

> **FastAPI Async (raw):** asyncpg puro, sem ORM, retornando dicts. **FastAPI Async (ORM):** SQLAlchemy async ORM + Pydantic validation nos responses (caso mais comum).

**Observações:**

- MVC entregou **maior throughput bruto** (2.953 req/s), seguido pelo FastAPI raw (1.870 req/s)
- FastAPI raw teve a **menor mediana** (10.93ms), mostrando a eficiência do event loop do asyncio para queries individuais
- FastAPI ORM apresentou **22% de erros** sob carga constante de 200 VUs — o overhead do SQLAlchemy + Pydantic satura o event loop do Python, causando timeouts no nginx. É a diferença entre "benchmark otimizado" e "aplicação real"
- A versão raw tem **25% mais throughput** que a versão ORM e **praticamente zero erros**

---

## 2. Ramp-up
 
**Configuração:** 5 estágios, 0 → 500 VUs em ~80 segundos.
 
```
0  →  50 VUs em 10s   (aquecimento)
50 → 150 VUs em 20s   (carga moderada)
150→ 300 VUs em 20s   (carga alta)
300→ 500 VUs em 20s   (stress)
500→   0 VUs em 10s   (recuperação)
```
 
**Objetivo:** encontrar o ponto onde cada backend começa a degradar.
 
| Métrica | Spring MVC | Spring WebFlux | FastAPI Async (raw) | FastAPI Async (ORM) |
|---|---|---|---|---|---|
| Throughput | 2.969 req/s | 2.189 req/s | 933 req/s | 1.560 req/s |
| Latência média | 72.67ms | 100.32ms | 241.34ms | 143.24ms |
| Latência mediana (p50) | 55.51ms | 20.64ms | 10.70ms | 39.66ms |
| Latência p90 | 174.81ms | 47.14ms | 114.21ms | 204.47ms |
| Latência p95 | 201.35ms | 54.30ms | 239.66ms | 449.34ms |
| Latência máxima | 773ms | 4.97s | 12.91s | 7.76s |
| Total de requisições | 237.555 | 179.250 | 80.405 | 124.815 |
| Iterações completas | 79.185 | 59.750 | 26.801 | 41.605 |
| Erros | 31 (0.01%) | 0 (0.00%) | 8 (0.01%) | 17.812 (14.27%) |
| Dados recebidos | 714 MB | 503 MB | 226 MB | 247 MB |

**Observações:**
- Versão ORM teve **mais throughput que a raw** neste cenário (1.560 vs 933 req/s) — o ramp-up progressivo permitiu que o pool de conexões se ajustasse melhor
- Porém, a versão ORM teve **14% de erros** contra ~0% da raw — o overhead aparece na forma de timeouts sob escalada
- MVC manteve o maior throughput sem erros significativos

---

## 3. Spike
 
**Configuração:** carga normal → pico repentino → recuperação.
 
```
0  →  50 VUs em 10s   (aquecimento)
50 →  50 VUs por 20s  (baseline estável)
50 → 500 VUs em 5s    (PICO)
500→ 500 VUs por 10s  (sustenta o pico)
500→  50 VUs em 5s    (volta ao normal)
50 →  50 VUs por 20s  (recuperação)
50 →   0 VUs em 5s    (fim)
```
 
**Objetivo:** medir resiliência — o backend absorve o pico? Se recupera depois?
 
| Métrica | Spring MVC | Spring WebFlux | FastAPI Async (raw) | FastAPI Async (ORM) |
|---|---|---|---|---|---|
| Throughput | 1.612 req/s | 1.686 req/s | 1.219 req/s | 1.085 req/s |
| Latência média | 50.72ms | 49.79ms | 91.59ms | 108.28ms |
| Latência mediana (p50) | 11.02ms | 2.44ms | 2.88ms | 5.31ms |
| Latência p90 | 163.90ms | 23.78ms | 30.94ms | 193.89ms |
| Latência p95 | 178.00ms | 35.08ms | 95.51ms | 672.50ms |
| Latência máxima | 671ms | 4.68s | 11.47s | 5.57s |
| Total de requisições | 121.004 | 126.597 | 94.658 | 81.522 |
| Iterações completas | 40.334 | 42.199 | 31.546 | 27.174 |
| Erros | 0 (0.00%) | 0 (0.00%) | 9 (0.01%) | 7.882 (9.66%) |
| Dados recebidos | 364 MB | 355 MB | 266 MB | 244 MB |

**Observações:**
- WebFlux manteve a liderança em throughput e a menor latência em todas as métricas
- FastAPI raw teve mediana de 2.88ms, quase empatando com WebFlux (2.44ms)
- FastAPI ORM apresentou **9.66% de erros** no spike — o overhead do ORM + Pydantic sob pico de 500 VUs gera timeouts
- A diferença entre raw e ORM mostra o **custo real do "caso comum"** em FastAPI

---

## Resumo Comparativo (FastAPI Async raw vs ORM)

| Métrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| **Throughput raw vs ORM** | 1.870 vs 1.495 (**1.25x**) | 933 vs 1.560 (ORM **1.67x**) | 1.219 vs 1.085 (**1.12x**) |
| **Erros raw vs ORM** | 0.01% vs **22.19%** | 0.01% vs **14.27%** | 0.01% vs **9.66%** |
| **Mediana raw vs ORM** | **10.93ms** vs 83.05ms | **10.70ms** vs 39.66ms | **2.88ms** vs 5.31ms |

> **RAW:** asyncpg puro, sem ORM, dicts. **ORM:** SQLAlchemy async + Pydantic (caso mais comum).

### Conclusão

- **Spring MVC** e **Spring WebFlux** continuam superiores em throughput bruto e latência, sem erros significativos em nenhum cenário.
- **FastAPI Async (raw)** com asyncpg puro é surpreendentemente competitivo: throughput entre 1.1x e 1.6x abaixo dos backends JVM, e mediana menor em Steady e Ramp-up. O preço é uma cauda longa (máximas de 9-12s) devido à contenção no pool asyncpg.
- **FastAPI Async (ORM)** com SQLAlchemy + Pydantic representa o **caso real de uso**. Os números são bem diferentes: 14-22% de erros sob carga, latências p95 muito maiores, throughput 1.1-1.25x menor que a versão raw. O overhead do ORM + validação Pydantic satura o event loop do Python, causando timeouts.
- **A escolha entre raw e ORM é a diferença entre benchmark e produção.** Asyncpg puro maximiza performance mas sacrifica produtividade. SQLAlchemy + Pydantic é o padrão da indústria, mas tem custo real em cenários de alta concorrência.

---
