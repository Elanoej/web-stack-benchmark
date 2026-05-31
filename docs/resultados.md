# Resultados do Bencharks

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
| Throughput | 2.082 req/s | 2.463 req/s |
| Latência média | 95.63ms | 80.93ms |
| Latência mediana (p50) | 98.55ms | 33.52ms |
| Latência p90 | 206.18ms | 64.54ms |
| Latência p95 | 284.41ms | 100.22ms |
| Latência máxima | 2.22s | 3.8s |
| Total de requisições | 62.736 | 77.364 |
| Iterações completas | 20.912 | 25.788 |
| Erros | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 198 MB | 228 MB |

**Obbservações:**

- Webflux entregou **18% mais requisições** no mesmo período
- Latência p95 do WebFlux foi **2.8x menor** que o MVC
- O MVC teve latência máxima menor (2.22s vs 3.8s) — pode indicar variação pontual de GC ou cold start do pool R2DBC

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
| Throughput | 1.982 req/s | 2.435 req/s |
| Latência média | 109.2ms | 89.05ms |
| Latência mediana (p50) | 49.66ms | 16.59ms |
| Latência p90 | 198.85ms | 42.43ms |
| Latência p95 | 268.62ms | 48.05ms |
| Latência máxima | 3.5s | 4.82s |
| Total de requisições | 160.824 | 201.825 |
| Iterações completas | 53.608 | 67.275 |
| Erros | 37 (0.02%) | 0 (0.00%) |
| Dados recebidos | 507 MB | 594 MB |

**Observações:**
- WebFlux completou **25% mais iterações** durante o ramp-up
- Latência p95 do WebFlux foi **5.6x menor** que o MVC
- **O MVC teve 37 falhas** — o WebFlux zerou. Esse é o sinal de thread pool exhaustion: quando a carga se aproximou de 500 VUs, o MVC não tinha threads disponíveis e começou a rejeitar requisições. O WebFlux não tem esse limite fixo
- O endpoint `/users/search` concentrou a maioria das falhas do MVC (30 de 37) — faz sentido, é a query mais pesada e ocupa a thread por mais tempo

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
| Throughput | 1.490 req/s | 1.696 req/s |
| Latência média | 58.14ms | 49.77ms |
| Latência mediana (p50) | 11.62ms | 2.38ms |
| Latência p90 | 182.6ms | 20.3ms |
| Latência p95 | 209.28ms | 35.38ms |
| Latência máxima | 1.38s | 4.67s |
| Total de requisições | 111.804 | 127.311 |
| Iterações completas | 37.268 | 42.437 |
| Erros | 0 (0.00%) | 0 (0.00%) |
| Dados recebidos | 353 MB | 375 MB |
 
**Observações:**
- Latência p90 do WebFlux foi **9x menor** durante o spike
- Latência mediana: 11.62ms (MVC) vs 2.38ms (WebFlux) — **5x menor**
- Ambos zeraram erros — os dois sobreviveram ao pico
- O MVC teve latência máxima menor (1.38s vs 4.67s) — pode indicar que o WebFlux teve alguma requisição presa durante o pico antes do event loop retomar

---
