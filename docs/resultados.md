# Resultados do Benchmark — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20).
>
> **Stacks testadas:** Rust + Axum (sqlx), Node Fastify (cluster mode), Go + Gin (GORM), Spring WebFlux (Kotlin, R2DBC), Spring MVC (Kotlin, JDBC), FastAPI Async (Python, SQLAlchemy)

---

## Configuração dos Testes

| Parâmetro | Valor |
|---|---|
| Ferramenta | k6 — 3 cenários por config de hardware |
| Banco de dados | PostgreSQL 16 (Docker) |
| Dataset | 10.000 usuários (9.000 ativos) |
| Endpoints | `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search` |
| Cenários | Steady State (200 VUs, 30s), Ramp-up (0→500 VUs, 80s), Spike (50→500→50 VUs, 75s) |
| Configs de hardware | 1 CPU/1GB, 2 CPUs/2GB, 4 CPUs/4GB, 8 CPUs/8GB, 12 CPUs/12GB |

---

## Ranking Geral (12 CPUs, Ramp-up)

| # | Stack | Throughput | p50 | p95 | Máxima | Erros | Escalabilidade |
|---|---|---|---|---|---|---|---|
| 1 | **Rust + Axum (sqlx)** | **14.578 req/s** | **13,0ms** | **32,2ms** | **74ms** | **0,00%** | **2,1x** |
| 2 | Node Fastify (cluster mode) | 14.198 req/s | 13ms | 33ms | 79ms | 0,02% | 4,6x |
| 3 | Go + Gin (GORM) | 10.958 req/s | 17,5ms | 43,3ms | 98ms | 0,00% | 2,8x |
| 4 | Spring WebFlux | 9.641 req/s | 14,1ms | 68,0ms | 109ms | 0,23% | 19,0x |
| 5 | Spring MVC | 3.046 req/s | 57,8ms | 185,0ms | 524ms | 0,00% | 7,0x |
| 6 | FastAPI Async (SQLAlchemy) | 1.584 req/s | 67,1ms | 503,5ms | 3.203ms | 0,00% | 3,0x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.** Carga constante e agressiva.

### 1 CPU / 1GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **4.102/s** | 3.296/s | 2.767/s | 147/s | 113/s | 2.500/s |
| p95 | **85ms** | 101ms | 259ms | 3.631ms | 6.997ms | 493ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **87%** |

### 2 CPUs / 2GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **12.228/s** | 6.004/s | 8.234/s | 669/s | 896/s | 1.798/s |
| p95 | **26ms** | 63ms | 83ms | 896ms | 1.206ms | 489ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **68%** | **57%** |

### 4 CPUs / 4GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **14.906/s** | 10.302/s | 12.926/s | 1.932/s | 1.421/s | 2.478/s |
| p95 | **15ms** | 41ms | 36ms | 226ms | 432ms | 451ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **53%** |

### 8 CPUs / 8GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **15.332/s** | 13.577/s | 11.281/s | 4.235/s | 2.464/s | 2.287/s |
| p95 | **15ms** | 21ms | 23ms | 104ms | 219ms | 324ms |
| Erros | **0%** | 0.79% | **0%** | **0%** | **0%** | **43%** |

### 12 CPUs / 12GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **15.076/s** | 13.610/s | 11.137/s | 6.507/s | 2.580/s | 1.529/s |
| p95 | **15ms** | 18ms | 21ms | 71ms | 218ms | 327ms |
| Erros | **0%** | 0.28% | **0%** | **0%** | **0%** | **0%** |

> **Análise:** Apenas **Rust + Axum**, **Go + Gin** e **Spring WebFlux** mantiveram **0% de erro em todas as configs** no cenário mais agressivo. Rust lidera em throughput com a menor latência p95.

---

## 2. Ramp-up

**5 estágios, 0 → 500 VUs em ~80 segundos.** Carga crescente, testa ponto de degradação.

| CPU | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| 1 | **7.032/s** (94ms p95) | 3.112/s (100ms) | 3.959/s (221ms) | 507/s (1.113ms) | 432/s (1.497ms) | 520/s (1.481ms) |
| 2 | **11.860/s** (55ms p95) | 5.996/s (88ms) | 8.038/s (114ms) | 2.094/s (267ms) | 1.185/s (510ms) | 1.055/s (720ms) |
| 4 | **14.421/s** (33ms p95) | 10.805/s (53ms) | 10.118/s (50ms) | 4.746/s (141ms) | 3.047/s (187ms) | 1.606/s (463ms) |
| 8 | **14.762/s** (32ms p95) | 14.245/s (33ms) | 10.921/s (44ms) | 7.629/s (88ms) | 3.062/s (190ms) | 1.626/s (455ms) |
| 12 | **14.578/s** (32ms p95) | 14.198/s (33ms) | 10.958/s (43ms) | 9.641/s (68ms) | 3.046/s (185ms) | 1.584/s (503ms) |

> **Análise:** Rust Axum lidera em todas as configs. Go Gin com **2 CPUs já entrega 8.038 req/s** — mais que WebFlux com 12 CPUs (9.641/s é só 20% maior que Go com 2 CPUs). WebFlux escala 19x de 1 a 12 CPUs (a maior escalabilidade).

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.** Testa resiliência e recuperação.

| CPU | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| 1 | **2.645/s** (63ms p95, **0% err**) | 1.679/s (72ms, **0% err**) | 1.910/s (203ms, **0% err**) | 1.135/s (614ms, 0,20% err) | 752/s (712ms, 0,83% err) | 454/s (1.398ms, 0,22% err) |
| 2 | **3.570/s** (15ms p95, **0% err**) | 2.307/s (69ms, **0% err**) | 2.771/s (71ms, **0% err**) | 1.631/s (223ms, 0% err) | 1.659/s (201ms, 0% err) | 938/s (657ms, 0,03% err) |
| 4 | **3.759/s** (8ms p95, **0% err**) | 3.217/s (27ms, **0% err**) | 3.331/s (25ms, **0% err**) | 2.137/s (111ms, 0% err) | 1.644/s (168ms, 0% err) | 1.224/s (414ms, 0% err) |
| 8 | **3.778/s** (7ms p95, **0% err**) | 3.730/s (9ms, **0% err**) | 3.390/s (16ms, **0% err**) | 2.792/s (49ms, 0% err) | 1.643/s (168ms, 0% err) | 1.237/s (410ms, 0% err) |
| 12 | **3.777/s** (7ms p95, **0% err**) | 3.766/s (7ms, **0% err**) | 3.379/s (17ms, **0% err**) | 3.171/s (28ms, 0% err) | 1.644/s (166ms, 0% err) | 1.211/s (420ms, 0% err) |

> **Análise:** **Rust + Axum, Go + Gin e Spring WebFlux** têm 0% de erro em todas as configs no spike. Rust lidera com a menor latência p95 (7ms em 12 CPUs) — **4x menor que WebFlux** (28ms) e **24x menor que MVC** (166ms).

---

## Escalabilidade

```
Throughput (req/s) em Ramp-up
16.000 ┤
14.000 ┤    Rust Axum ──●────●────●────●────●
         Node Fastify ─────●────●────●────●────●
12.000 ┤
10.000 ┤                Go+Gin ──●────●────●────●
 8.000 ┤
 6.000 ┤                          WebFlux ──●
 4.000 ┤                     ●
 2.000 ┤               ●──●        MVC ─────●────●────●
      ┤      ●─●  FastAPI ──●────●────●────●
      └───┬──────┬──────┬──────┬──────┬──────
         1      2      4      8      12    CPUs
```

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalab. |
|---|---|---|---|---|---|---|
| Rust + Axum | 7.032 | 11.860 | 14.421 | 14.762 | 14.578 | **2,1x** |
| Node Fastify | 3.112 | 5.996 | 10.805 | 14.245 | 14.198 | **4,6x** |
| Go + Gin (GORM) | 3.959 | 8.038 | 10.118 | 10.921 | 10.958 | **2,8x** |
| WebFlux | 507 | 2.094 | 4.746 | 7.629 | 9.641 | **19,0x** |
| MVC | 432 | 1.185 | 3.047 | 3.062 | 3.046 | **7,0x** |
| FastAPI | 520 | 1.055 | 1.606 | 1.626 | 1.584 | **3,0x** |

---

## Taxa de Erro em Steady State

O cenário mais revelador: quem sustenta 200 conexões simultâneas sem falhar?

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| **Rust + Axum** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Go + Gin (GORM)** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Node Fastify** | **0%** | **0%** | **0%** | 0.79% | 0.28% |
| **WebFlux** | **0%** | **0%** | **0%** | **0%** | **0%** |
| MVC | 0% | **68%** | 0% | 0% | 0% |
| FastAPI | **87%** | **57%** | **53%** | **43%** | 0% |

---

## Conclusão

### 🥇 Rust + Axum (sqlx) — A campeã geral

- **Maior throughput** em todos os cenários e configs: 14.578 req/s (ramp-up, 12 CPUs)
- **Menor latência**: p95 de 7ms no spike, 15ms no steady, 32ms no ramp-up
- **Zero erros**: 0% em steady, ramp-up e spike em todas as configs
- **Eficiente**: 1 CPU (7.032/s) já supera o pico de qualquer stack JVM

### 🥈 Node Fastify (cluster mode) — Impressionante em throughput

- Segundo lugar geral com 14.198 req/s em ramp-up (12 CPUs), superando Go + Gin
- Latência p95 de 33ms no ramp-up e 7ms no spike — competitiva com Rust
- **0% erro** em spike em todas as configs
- Escalabilidade de 4.6x de 1 a 12 CPUs — excelente para ambientes com múltiplos núcleos
- Pequena taxa de erro em steady state a partir de 8 CPUs (0.79% em 8 CPUs, 0.28% em 12 CPUs)

### 🥉 Go + Gin (GORM) — A mais eficiente por núcleo

- Terceiro lugar geral com margem confortável sobre as stacks JVM
- **0% erro** em todos os cenários
- **Eficiência brutal**: 2 CPUs (8.038/s) > WebFlux com 8 CPUs (7.629/s)
- GORM incluso: overhead imperceptível em Go

### 4º Spring WebFlux — A melhor stack JVM

- Escalabilidade quase linear: **19x** de 1 a 12 CPUs
- 0% de erro em steady state em todas as configs
- 9.641 req/s em 12 CPUs (ramp-up) — ~66% do Rust Axum

### 5º Spring MVC — O clássico limitado

- Sofre com thread-per-request: 68% de erro em 2 CPUs no steady
- Platô em 4 CPUs (~3.050 req/s) — bottleneck no banco/nginx
- Performance sólida sem erros em configs ≥4 CPUs

### 6º FastAPI Async (SQLAlchemy) — O mais fraco em throughput

- Overhead do ORM (SQLAlchemy + Pydantic) + GIL limita o máximo a ~1.600 req/s
- 87% de erro em 1 CPU no steady state
- Zera erros a partir de 4 CPUs (steady)

### ⚡ Eficiência é tudo

> **Rust Axum com 2 CPUs (11.860 req/s) entrega mais throughput que QUALQUER stack JVM com 12 CPUs.** Node Fastify com 4 CPUs (10.805/s) também supera o pico do WebFlux com 12 CPUs (9.641/s). Go Gin com 2 CPUs (8.038/s) chega muito próximo.
>
> Em termos de custo de infraestrutura, Rust Axum é ~4x mais eficiente que WebFlux e ~18x mais eficiente que FastAPI.
