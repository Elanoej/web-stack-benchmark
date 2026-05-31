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
| Throughput | 2.953 req/s | 2.226 req/s | 566 req/s |
| Latência média | 67.49ms | 89.59ms | 350.30ms |
| Latência mediana (p50) | 89.76ms | 24.40ms | 316.13ms |
| Latência p90 | 118.79ms | 37.04ms | 884.40ms |
| Latência p95 | 183.50ms | 46.35ms | 965.06ms |
| Latência máxima | 614ms | 4.37s | 3.38s |
| Total de requisições | 89.121 | 70.546 | 17.299 |
| Iterações completas | 29.707 | 23.515 | 5.766 |
| Erros | 0 (0.00%) | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 268 MB | 198 MB | 48 MB |

**Observações:**

- MVC entregou **33% mais requisições** que o WebFlux e **5.2x mais** que o FastAPI
- Latência p95 do WebFlux foi **4x menor** que o MVC (46ms vs 184ms) e **21x menor** que o FastAPI (46ms vs 965ms)
- FastAPI ficou ~5x mais lento que o MVC em todas as métricas — o overhead do SQLAlchemy async + asyncpg + GIL se soma para queries leves
- O FastAPI manteve 0% de erros, mas com throughput muito inferior

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
| Throughput | 2.969 req/s | 2.189 req/s | 577 req/s |
| Latência média | 72.67ms | 100.32ms | 381.63ms |
| Latência mediana (p50) | 55.51ms | 20.64ms | 82.66ms |
| Latência p90 | 174.81ms | 47.14ms | 1.13s |
| Latência p95 | 201.35ms | 54.30ms | 1.33s |
| Latência máxima | 773ms | 4.97s | 6.37s |
| Total de requisições | 237.555 | 179.250 | 46.203 |
| Iterações completas | 79.185 | 59.750 | 15.401 |
| Erros | 31 (0.01%) | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 714 MB | 503 MB | 130 MB |

**Observações:**
- MVC manteve throughput **36% maior** que o WebFlux e **5.1x maior** que o FastAPI
- FastAPI teve mediana baixa (82ms) mas p95 de 1.33s — distribuição com cauda longa, indicando contenção no pool de conexões async
- **O MVC teve 31 falhas** — o WebFlux e FastAPI zeraram. O FastAPI, por ser assíncrono, também não sofre de thread pool exhaustion
- FastAPI apresentou latência máxima de 6.37s — outliers ainda mais altos que o WebFlux

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
| Throughput | 1.612 req/s | 1.686 req/s | 358 req/s |
| Latência média | 50.72ms | 49.79ms | 358.66ms |
| Latência mediana (p50) | 11.02ms | 2.44ms | 65.56ms |
| Latência p90 | 163.90ms | 23.78ms | 1.22s |
| Latência p95 | 178.00ms | 35.08ms | 1.34s |
| Latência máxima | 671ms | 4.68s | 8.01s |
| Total de requisições | 121.004 | 126.597 | 26.884 |
| Iterações completas | 40.334 | 42.199 | 8.961 |
| Erros | 0 (0.00%) | 0 (0.00%) | 142 (0.53%) |
| Dados recebidos | 364 MB | 355 MB | 75 MB |
  
**Observações:**
- WebFlux teve **5% mais throughput** que o MVC — FastAPI ficou **4.7x abaixo** do WebFlux
- FastAPI foi o **único com erros no spike**: 0.53% (142 requisições rejeitadas em ~27k), sinal de que o pool de conexões R2DBC não sustentou o pico de 500 VUs
- Latência p95: 35ms (WebFlux) vs 178ms (MVC) vs 1.34s (FastAPI) — **WebFlux 38x menor que FastAPI**
- FastAPI apresentou outliers extremos de 8s — o dobro do WebFlux

---

## Resumo Comparativo

| Métrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| **Throughput** | MVC +33% / WF **5.2x > FA** | MVC +36% / WF **3.8x > FA** | WebFlux +5% / WF **4.7x > FA** |
| **Latência mediana** | WF 3.7x < MVC / WF **13x < FA** | WF 2.7x < MVC / WF **4x < FA** | WF 4.5x < MVC / WF **27x < FA** |
| **Latência p95** | WF 4x < MVC / WF **21x < FA** | WF 3.7x < MVC / WF **24x < FA** | WF 5x < MVC / WF **38x < FA** |
| **Erros** | Todos 0% | MVC 0.01% / WF 0% / FA 0% | MVC 0% / WF 0% / FA 0.53% |

> FA = FastAPI Async

### Conclusão

- **Spring MVC** entregou **maior throughput bruto** em todos os cenários (exceto Spike, onde o WebFlux liderou por pouco). O bloqueante JDBC + thread pool do Tomcat é extremamente eficiente para queries leves.
- **Spring WebFlux** teve **latências muito menores** que ambos os concorrentes em todas as métricas (p50, p90, p95). O modelo reativo brilha especialmente no Spike: p95 de 35ms vs 178ms (MVC) vs 1.34s (FastAPI).
- **FastAPI Async** ficou **significativamente atrás** em throughput e latência. O overhead do SQLAlchemy async + asyncpg + GIL do Python se soma, resultando em ~5x menos requisições que os backends JVM. A mediana baixa no Ramp-up (82ms) e Spike (65ms) mostra que o event loop do Python funciona bem para queries individuais, mas a cauda longa (p95 > 1s) indica contenção no pool de conexões.
- O FastAPI foi o **único com erros no Spike** (0.53%), sinal de que o pool R2DBC padrão não sustentou o pico de 500 VUs — mesmo comportamento de thread pool exhaustion do MVC, mas no pool de conexões.
- **JVM vs Python**: em todas as métricas, os backends em JVM (MVC e WebFlux) superaram o FastAPI por uma margem de 3x a 38x em latência e 4x a 5x em throughput.

---
