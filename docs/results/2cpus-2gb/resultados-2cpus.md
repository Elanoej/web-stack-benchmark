# Resultados — 2 CPUs / 2GB RAM

> **Ambiente:** 2 CPUs, 2GB RAM por container. PostgreSQL via Docker.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State

**200 VUs simultâneos, 30 segundos, sem sleep.**

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput (req/s) | 379 | 606 | 1.023 |
| Latência média (ms) | 522.64 | 328.24 | 194.41 |
| Latência p50 (ms) | 189.62 | 300.47 | 195.93 |
| Latência p90 (ms) | 1.408 | 610.63 | 355.70 |
| Latência p95 (ms) | 1.989 | 987.79 | 504.49 |
| Latência máxima (ms) | 6.198 | 3.501 | 2.732 |
| Total requisições | 11.604 | 18.414 | 31.020 |
| Erros | 0.00% | 0.00% | 0.00% |

**Observação:** Com 2 CPUs, FastAPI lidera em throughput — 3 workers concorrem bem com o event loop. Spring MVC sofre com contenção de threads (thread-per-request).

---

## Ramp-up

**5 estágios: 0 → 50 → 150 → 300 → 500 → 0 VUs em ~80s.**

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput (req/s) | 1.142 | 1.894 | 1.044 |
| Latência média (ms) | 189.78 | 114.05 | 208.55 |
| Latência p50 (ms) | 124.67 | 105.92 | 103.91 |
| Latência p90 (ms) | 481.97 | 254.05 | 579.20 |
| Latência p95 (ms) | 571.44 | 272.31 | 679.54 |
| Latência máxima (ms) | 2.329 | 308 | 3.981 |
| Total requisições | 91.401 | 151.512 | 83.499 |
| Erros | 0.03% | 0.00% | 0.00% |

**Observação:** WebFlux domina — modelo reativo escala até 500 VUs sem degradação significativa (máxima de 308ms). FastAPI e MVC ficam próximos.

---

## Spike

**Pico abrupto: 50 → 500 VUs em 5s, sustenta, volta ao normal.**

| Métrica | Spring MVC | Spring WebFlux | FastAPI Async |
|---|---|---|---|
| Throughput (req/s) | 1.369 | 1.621 | 896 |
| Latência média (ms) | 75.10 | 50.40 | 119.99 |
| Latência p50 (ms) | 11.07 | 1.77 | 11.16 |
| Latência p90 (ms) | 186.66 | 215.55 | 538.23 |
| Latência p95 (ms) | 213.71 | 226.90 | 691.96 |
| Latência máxima (ms) | 5.053 | 280 | 4.020 |
| Total requisições | 102.723 | 121.626 | 67.236 |
| Erros | 0.00% | 0.00% | 0.01% |

**Observação:** WebFlux tem a latência máxima mais baixa (280ms) — sem cauda longa. MVC tem p95 baixo (214ms) mas máxima alta. FastAPI sofre com cauda longa no pico.

---

## Resumo

| Cenário | Vencedor | Destaque |
|---|---|---|
| Steady State | **FastAPI** | 1.023 req/s com p95 de 504ms |
| Ramp-up | **WebFlux** | 1.894 req/s, latência máxima de apenas 308ms |
| Spike | **WebFlux** | 1.621 req/s, sem cauda longa (max 280ms) |

**Conclusão:** Com 2 CPUs, a vantagem do WebFlux é clara em cenários de carga variável. FastAPI surpreende no steady state. MVC sofre com a contenção de threads do modelo bloqueante em CPUs limitadas.
