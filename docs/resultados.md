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
  
| Métrica | Spring MVC | Spring WebFlux |
|---|---|---|
| Throughput | 2.953 req/s | 2.226 req/s |
| Latência média | 67.49ms | 89.59ms |
| Latência mediana (p50) | 89.76ms | 24.40ms |
| Latência p90 | 118.79ms | 37.04ms |
| Latência p95 | 183.50ms | 46.35ms |
| Latência máxima | 614ms | 4.37s |
| Total de requisições | 89.121 | 70.546 |
| Iterações completas | 29.707 | 23.515 |
| Erros | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 268 MB | 198 MB |

**Observações:**

- MVC entregou **33% mais requisições** que o WebFlux no steady state
- Latência p95 do WebFlux foi **4x menor** que o MVC (46ms vs 184ms)
- Latência mediana: 89.76ms (MVC) vs 24.40ms (WebFlux) — **WebFlux 3.7x mais rápido na mediana**
- O MVC teve latência máxima muito menor (614ms vs 4.37s) — o WebFlux apresentou outliers altos que puxam a média pra cima, provavelmente GC do JDK 21 ou warmup do pool R2DBC

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
 
| Métrica | Spring MVC | Spring WebFlux |
|---|---|---|
| Throughput | 2.969 req/s | 2.189 req/s |
| Latência média | 72.67ms | 100.32ms |
| Latência mediana (p50) | 55.51ms | 20.64ms |
| Latência p90 | 174.81ms | 47.14ms |
| Latência p95 | 201.35ms | 54.30ms |
| Latência máxima | 773ms | 4.97s |
| Total de requisições | 237.555 | 179.250 |
| Iterações completas | 79.185 | 59.750 |
| Erros | 31 (0.01%) | 0 (0.00%) |
| Dados recebidos | 714 MB | 503 MB |

**Observações:**
- MVC manteve throughput **36% maior** que o WebFlux durante o ramp-up
- Latência mediana do WebFlux foi **2.7x menor** (20.64ms vs 55.51ms)
- Latência p95 do WebFlux foi **3.7x menor** (54ms vs 201ms)
- **O MVC teve 31 falhas** — o WebFlux zerou. É o sinal clássico de thread pool exhaustion: quando a carga se aproximou de 500 VUs, o MVC começou a rejeitar requisições por falta de threads no pool do Tomcat. O WebFlux (reativo) não tem esse limite fixo
- Novamente, o WebFlux apresentou latência máxima alta (~5s), indicando outliers esporádicos

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
 
| Métrica | Spring MVC | Spring WebFlux |
|---|---|---|
| Throughput | 1.612 req/s | 1.686 req/s |
| Latência média | 50.72ms | 49.79ms |
| Latência mediana (p50) | 11.02ms | 2.44ms |
| Latência p90 | 163.90ms | 23.78ms |
| Latência p95 | 178.00ms | 35.08ms |
| Latência máxima | 671ms | 4.68s |
| Total de requisições | 121.004 | 126.597 |
| Iterações completas | 40.334 | 42.199 |
| Erros | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 364 MB | 355 MB |
  
**Observações:**
- WebFlux teve **5% mais throughput** que o MVC durante o spike — única categoria onde superou o MVC
- Latência p90 do WebFlux foi **6.9x menor** (24ms vs 164ms)
- Latência mediana: 11.02ms (MVC) vs 2.44ms (WebFlux) — **WebFlux 4.5x mais rápido**
- Latência p95: 178ms (MVC) vs 35ms (WebFlux) — **WebFlux 5x menor**
- Ambos zeraram erros — os dois sobreviveram ao pico
- O padrão dos outliers altos do WebFlux se repetiu: latência máxima de 4.68s, provavelmente GC pause

---

## Resumo Comparativo

| Métrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| **Throughput** | MVC +33% | MVC +36% | WebFlux +5% |
| **Latência mediana** | WebFlux 3.7x menor | WebFlux 2.7x menor | WebFlux 4.5x menor |
| **Latência p95** | WebFlux 4x menor | WebFlux 3.7x menor | WebFlux 5x menor |
| **Erros** | Ambos 0% | MVC 0.01% / WF 0% | Ambos 0% |

### Conclusão

- **Spring MVC** entregou **maior throughput bruto** nos cenários de carga constante e progressiva (Steady e Ramp-up). O bloqueante JDBC + thread pool do Tomcat conseguiu extrair mais requisições por segundo que o modelo reativo.
- **Spring WebFlux** teve **latências muito menores** em todas as métricas (p50, p90, p95), especialmente no Spike. O modelo reativo não sofre de thread pool exhaustion e se recupera melhor após picos de carga.
- O WebFlux apresentou **outliers de latência máxima** altos (4-5s) em todos os cenários — provavelmente GC pause do JDK 21 ou warmup do pool R2DBC. Isso puxou a latência média (avg) para cima, mas a mediana e os percentis baixos refletem melhor a experiência real.
- **No Spike**, o WebFlux foi superior tanto em throughput quanto em latência — o modelo reativo brilha em cenários de carga explosiva.
- O MVC apresentou **0.01% de erros** no Ramp-up (31 requisições rejeitadas em ~237k), sinal de exhaustion do thread pool ao se aproximar de 500 VUs. O WebFlux zerou erros em todos os cenários.

---
