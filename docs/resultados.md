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

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput | 2.953 req/s | 2.226 req/s | 1.495 req/s |
| Latência média | 67.49ms | 89.59ms | 132.57ms |
| Latência mediana (p50) | 89.76ms | 24.40ms | 83.05ms |
| Latência p90 | 118.79ms | 37.04ms | 198.33ms |
| Latência p95 | 183.50ms | 46.35ms | 287.54ms |
| Latência máxima | 614ms | 4.37s | 5.12s |
| Total de requisições | 89.121 | 70.546 | 45.471 |
| Iterações completas | 29.707 | 23.515 | 15.157 |
| Erros | 0 (0.00%) | 0 (0.00%) | 10.092 (22.19%) |
| Dados recebidos | 268 MB | 198 MB | 85 MB |

> FastAPI Async configurado com SQLAlchemy async ORM + Pydantic (caso mais comum de uso).

**Observações:**

- MVC entregou **maior throughput bruto** (2.953 req/s) e **zero erros**
- FastAPI ORM apresentou **22% de erros** sob carga constante de 200 VUs — o overhead do ORM + Pydantic satura o event loop do Python, causando timeouts no nginx
- WebFlux manteve a menor latência p95 (46ms), mostrando a vantagem do modelo reativo

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

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput | 2.969 req/s | 2.189 req/s | 1.560 req/s |
| Latência média | 72.67ms | 100.32ms | 143.24ms |
| Latência mediana (p50) | 55.51ms | 20.64ms | 39.66ms |
| Latência p90 | 174.81ms | 47.14ms | 204.47ms |
| Latência p95 | 201.35ms | 54.30ms | 449.34ms |
| Latência máxima | 773ms | 4.97s | 7.76s |
| Total de requisições | 237.555 | 179.250 | 124.815 |
| Iterações completas | 79.185 | 59.750 | 41.605 |
| Erros | 31 (0.01%) | 0 (0.00%) | 17.812 (14.27%) |
| Dados recebidos | 714 MB | 503 MB | 247 MB |

**Observações:**
- MVC manteve o maior throughput (2.969 req/s) e erros mínimos
- FastAPI ORM teve **14% de erros** — o overhead do ORM + Pydantic causa timeouts sob escalada de VUs
- WebFlux teve a menor latência p50 (20ms) e p95 (54ms), sem erros

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

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput | 1.612 req/s | 1.686 req/s | 1.085 req/s |
| Latência média | 50.72ms | 49.79ms | 108.28ms |
| Latência mediana (p50) | 11.02ms | 2.44ms | 5.31ms |
| Latência p90 | 163.90ms | 23.78ms | 193.89ms |
| Latência p95 | 178.00ms | 35.08ms | 672.50ms |
| Latência máxima | 671ms | 4.68s | 5.57s |
| Total de requisições | 121.004 | 126.597 | 81.522 |
| Iterações completas | 40.334 | 42.199 | 27.174 |
| Erros | 0 (0.00%) | 0 (0.00%) | 7.882 (9.66%) |
| Dados recebidos | 364 MB | 355 MB | 244 MB |

**Observações:**
- WebFlux liderou em throughput (1.686 req/s) e teve a menor latência em todas as métricas
- FastAPI ORM apresentou **9.66% de erros** — o overhead do ORM + Pydantic sob pico de 500 VUs gera timeouts
- MVC manteve zero erros e latência p95 de 178ms

---

## Comparativo: FastAPI raw vs ORM

Para referência, a diferença entre a versão otimizada (asyncpg puro, sem ORM) e a versão com SQLAlchemy + Pydantic usada nas tabelas acima:

| Métrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| throughput raw | 1.870 req/s | 933 req/s | 1.219 req/s |
| throughput ORM | 1.495 req/s | 1.560 req/s | 1.085 req/s |
| erros raw | 0.01% | 0.01% | 0.01% |
| erros ORM | **22.19%** | **14.27%** | **9.66%** |
| mediana raw | **10.93ms** | **10.70ms** | **2.88ms** |
| mediana ORM | 83.05ms | 39.66ms | 5.31ms |

### Conclusão

- **Spring MVC** e **Spring WebFlux** são superiores em throughput e latência, sem erros significativos
- **FastAPI Async (ORM)** — SQLAlchemy + Pydantic, o caso mais comum — apresenta **10-22% de erros** sob carga alta e latências p95 entre 287ms e 672ms. O overhead do ORM + validação satura o event loop do Python, causando timeouts no nginx
- **FastAPI Async (raw)** com asyncpg puro é competitivo (1.1x-1.6x abaixo dos backends JVM em throughput) e tem mediana menor que MVC em todos cenários, mas paga o preço com cauda longa (máximas de 9-12s)
- **A diferença entre raw e ORM é o gap entre benchmark e produção:** asyncpg puro maximiza performance; SQLAlchemy + Pydantic é o padrão da indústria com custo real em concorrência

---
