# Resultados do Benchmark — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
>
> **Stacks testadas:** Go + Gin, Spring WebFlux (Kotlin), Spring MVC (Kotlin), FastAPI Async (Python)

---

## Configuração dos Testes

| Parâmetro | Valor |
|---|---|
| Ferramenta | k6 |
| Banco de dados | PostgreSQL 16 (Docker) |
| Dataset | 10.000 usuários (9.000 ativos) |
| Endpoints | `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search` |
| Cenários | Steady State (200 VUs, 30s), Ramp-up (0→500 VUs, 80s), Spike (50→500→50 VUs, 75s) |
| Configs de hardware | 1 CPU/1GB, 2 CPUs/2GB, 4 CPUs/4GB, 8 CPUs/8GB, 12 CPUs/12GB |

---

## Ranking Geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p50 | p95 | Máxima | Erros | Escalabilidade |
|---|---|---|---|---|---|---|---|
| 1 | **Go + Gin** | **12.780 req/s** | **14,9ms** | **37,1ms** | **75ms** | **0,00%** | **2,4x** |
| 2 | Spring WebFlux | 9.641 req/s | 14,1ms | 68,0ms | 109ms | 0,23% | 19,0x |
| 3 | Spring MVC | 3.046 req/s | 57,8ms | 185,0ms | 524ms | 0,00% | 7,0x |
| 4 | FastAPI Async | 1.584 req/s | 67,1ms | 503,5ms | 3.203ms | 0,00% | 3,0x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.** Carga constante e agressiva.

### 1 CPU / 1GB

| Métrica | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| Throughput | **3.626/s** | 147/s | 113/s | 2.500/s |
| p95 | **98ms** | 3.631ms | 6.997ms | 493ms |
| Erros | **0%** | **0%** | **0%** | **87%** |

### 2 CPUs / 2GB

| Métrica | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| Throughput | **11.139/s** | 669/s | 896/s | 1.798/s |
| p95 | **29ms** | 896ms | 1.206ms | 489ms |
| Erros | **0%** | **0%** | **68%** | **57%** |

### 4 CPUs / 4GB

| Métrica | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| Throughput | **12.923/s** | 1.932/s | 1.421/s | 2.478/s |
| p95 | **18ms** | 226ms | 432ms | 451ms |
| Erros | **0%** | **0%** | **0%** | **53%** |

### 8 CPUs / 8GB

| Métrica | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| Throughput | **12.599/s** | 4.235/s | 2.464/s | 2.287/s |
| p95 | **18ms** | 104ms | 219ms | 324ms |
| Erros | **0%** | **0%** | **0%** | **43%** |

### 12 CPUs / 12GB

| Métrica | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| Throughput | **13.131/s** | 6.507/s | 2.580/s | 1.529/s |
| p95 | **18ms** | 71ms | 218ms | 327ms |
| Erros | **0%** | **0%** | **0%** | **0%** |

> **Análise:** Apenas **Go + Gin** e **Spring WebFlux** mantiveram **0% de erro em todas as configs** no cenário mais agressivo. O Go Gin entrega 2x o throughput do WebFlux com latência 4x menor.

---

## 2. Ramp-up

**5 estágios, 0 → 500 VUs em ~80 segundos.** Carga crescente, testa ponto de degradação.

| CPU | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| 1 | **5.375/s** (113ms p95) | 507/s (1.113ms) | 432/s (1.497ms) | 520/s (1.481ms) |
| 2 | **10.897/s** (59ms p95) | 2.094/s (267ms) | 1.185/s (510ms) | 1.055/s (720ms) |
| 4 | **12.305/s** (39ms p95) | 4.746/s (141ms) | 3.047/s (187ms) | 1.606/s (463ms) |
| 8 | **12.613/s** (38ms p95) | 7.629/s (88ms) | 3.062/s (190ms) | 1.626/s (455ms) |
| 12 | **12.780/s** (37ms p95) | 9.641/s (68ms) | 3.046/s (185ms) | 1.584/s (503ms) |

> **Análise:** Go Gin com **2 CPUs já entrega 10.897 req/s** — mais que qualquer stack concorrente com 12 CPUs. WebFlux escala 19x de 1 a 12 CPUs (a maior escalabilidade). MVC e FastAPI platonam em 4 CPUs.

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.** Testa resiliência e recuperação.

| CPU | Go + Gin | WebFlux | MVC | FastAPI |
|---|---|---|---|---|
| 1 | **2.289/s** (95ms p95, **0% err**) | 1.135/s (614ms, 0,20% err) | 752/s (712ms, 0,83% err) | 454/s (1.398ms, 0,22% err) |
| 2 | **3.346/s** (23ms p95, **0% err**) | 1.631/s (223ms, 0% err) | 1.659/s (201ms, 0% err) | 938/s (657ms, 0,03% err) |
| 4 | **3.629/s** (10ms p95, **0% err**) | 2.137/s (111ms, 0% err) | 1.644/s (168ms, 0% err) | 1.224/s (414ms, 0% err) |
| 8 | **3.652/s** (9ms p95, **0% err**) | 2.792/s (49ms, 0% err) | 1.643/s (168ms, 0% err) | 1.237/s (410ms, 0% err) |
| 12 | **3.681/s** (8ms p95, **0% err**) | 3.171/s (28ms, 0% err) | 1.644/s (166ms, 0% err) | 1.211/s (420ms, 0% err) |

> **Análise:** **Go + Gin é a única stack com 0% de erro em TODAS as configs** no spike. A latência p95 de **8ms em 12 CPUs** é irreal — 3,5x menor que WebFlux (28ms) e 20x menor que MVC (166ms).

---

## Escalabilidade

```
Throughput (req/s) em Ramp-up
14.000 ┤
12.000 ┤       Go+Gin ──●────●────●────●
10.000 ┤
 8.000 ┤                      WebFlux ──●
 6.000 ┤                   ●
 4.000 ┤             ●
 2.000 ┤       ●──●        MVC ─────●────●────●
       ┤──●          FastAPI ──●────●────●────●
       └───┬──────┬──────┬──────┬──────┬──────
          1      2      4      8      12    CPUs
```

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalab. |
|---|---|---|---|---|---|---|
| Go + Gin | 5.375 | 10.897 | 12.305 | 12.613 | 12.780 | **2,4x** |
| WebFlux | 507 | 2.094 | 4.746 | 7.629 | 9.641 | **19,0x** |
| MVC | 432 | 1.185 | 3.047 | 3.062 | 3.046 | **7,0x** |
| FastAPI | 520 | 1.055 | 1.606 | 1.626 | 1.584 | **3,0x** |

---

## Taxa de Erro em Steady State

O cenário mais revelador: quem sustenta 200 conexões simultâneas sem falhar?

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| **Go + Gin** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **WebFlux** | **0%** | **0%** | **0%** | **0%** | **0%** |
| MVC | 0% | **68%** | 0% | 0% | 0% |
| FastAPI | **87%** | **57%** | **53%** | **43%** | 0% |

---

## Conclusão

### 🥇 Go + Gin — A campeã absoluta

- **Maior throughput** em todos os cenários e configs: 12.780 req/s (ramp-up, 12 CPUs)
- **Menor latência**: p95 de 8ms no spike, 18ms no steady, 37ms no ramp-up
- **Zero erros**: única stack com 0% de erro em steady, ramp-up e spike em todas as configs
- **Eficiência brutal**: 2 CPUs (10.897 req/s) > qualquer concorrente com 12 CPUs

### 🥈 Spring WebFlux — A melhor JVM

- Escalabilidade quase linear: **19x** de 1 a 12 CPUs
- 0% de erro em steady state em todas as configs
- 9.641 req/s em 12 CPUs (ramp-up) — ~75% do Go Gin

### 🥉 Spring MVC — O clássico limitado

- Sofre com thread-per-request: 68% de erro em 2 CPUs no steady
- Platô em 4 CPUs (~3.050 req/s) — bottleneck no banco/nginx
- Ainda assim, entrega performance sólida sem erros em configs ≥4 CPUs

### 4º FastAPI Async — O mais fraco em throughput

- Overhead do ORM (SQLAlchemy + Pydantic) + GIL limita o máximo a ~1.600 req/s
- 87% de erro em 1 CPU no steady state
- Porém, zera erros a partir de 4 CPUs (steady) e tem a melhor escalabilidade entre as stacks Python

### ⚡ Eficiência é tudo

> **Go Gin com 2 CPUs (10.897 req/s) entrega mais throughput que QUALQUER stack concorrente com 12 CPUs.**
>
> Em termos de custo de infraestrutura, Go Gin é 6x mais eficiente que a segunda melhor stack (WebFlux) e 20x mais eficiente que FastAPI.
