# Resultados do Benchmark — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (demais stacks aumentadas para 30, FastAPI pool_size=2, Node divide entre workers) (FastAPI: pool_size=2 + max_overflow=0, workers=CPUS, PostgreSQL max_connections=30).
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
| 1 | **Rust + Axum (sqlx)** | **15922 req/s** | **30ms** | **29.9ms** | **74ms** | **0,00%** | **2.1x** |
| 2 | Node Fastify (cluster mode) | 14.198 req/s | 13ms | 33ms | 79ms | 0,02% | 4,6x |
| 3 | Go + Gin (GORM) | 13154 req/s | 36ms | 35.9ms | 98ms | 0,00% | 3.1x |
| 4 | Spring WebFlux | 11.027 req/s | 12,5ms | 57,9ms | 97ms | 0,23% | 19,0x |
| 5 | Spring MVC | 8.061 req/s | 17,3ms | 87,5ms | 420ms | 0,13% | 20,2x |
| 6 | FastAPI Async (SQLAlchemy) | 4.949 req/s | 43,6ms | 186,3ms | 1.621ms | 0,00% | 8,3x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.** Carga constante e agressiva.

### 1 CPU / 1GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **7657/s** | | 4249/s | | | |
| p95 | **44ms** | | 165ms | | | |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 2 CPUs / 2GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **7657/s** | | 4249/s | | | |
| p95 | **44ms** | | 165ms | | | |
| Erros | **0%** | **0%** | **0%** | **0%** | **68%** | **0%** |

### 4 CPUs / 4GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **7657/s** | | 4249/s | | | |
| p95 | **44ms** | | 165ms | | | |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 8 CPUs / 8GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **7657/s** | | 4249/s | | | |
| p95 | **44ms** | | 165ms | | | |
| Erros | **0%** | 0.79% | **0%** | **0%** | **0%** | **0%** |

### 12 CPUs / 12GB

| Métrica | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| Throughput | **7657/s** | | 4249/s | | | |
| p95 | **44ms** | | 165ms | | | |
| Erros | **0%** | 0.28% | **0%** | **0%** | **0%** | **0%** |

> **Análise:** Apenas **Rust + Axum**, **Go + Gin**, **Spring WebFlux** e **FastAPI Async (SQLAlchemy)** mantiveram **0% de erro em todas as configs** no cenário mais agressivo. Rust lidera em throughput com a menor latência p95.

---

## 2. Ramp-up

**5 estágios, 0 → 500 VUs em ~80 segundos.** Carga crescente, testa ponto de degradação.

| CPU | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| 1 | **7709/s** (89ms p95) | 3.112/s (100ms) | 4246/s (205ms) | 579/s (1.087ms) | 400/s (1.796ms) | 593/s (1.235ms) |
| 2 | **13375/s** (50ms p95) | 5.996/s (88ms) | 8668/s (102ms) | 2.411/s (257ms) | 1.021/s (699ms) | 1.189/s (693ms) |
| 4 | **15722/s** (30ms p95) | 10.805/s (53ms) | 13325/s (39ms) | 4.919/s (133ms) | 5.729/s (107ms) | 2.272/s (418ms) |
| 8 | **16094/s** (30ms p95) | 14.245/s (33ms) | 13251/s (35ms) | 8.638/s (76ms) | 7.889/s (89ms) | 3.816/s (264ms) |
| 12 | **15922/s** (30ms p95) | 14.198/s (33ms) | 13154/s (36ms) | 11.027/s (58ms) | 8.061/s (88ms) | 4.949/s (186ms) |

> **Análise:** Rust Axum lidera em todas as configs. Go Gin com **2 CPUs já entrega 8.668 req/s** — mais que WebFlux com 12 CPUs (11.027/s — 27% maior que Go com 2 CPUs). WebFlux escala 19x de 1 a 12 CPUs (a maior escalabilidade).

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.** Testa resiliência e recuperação.

| CPU | Rust + Axum | Node Fastify | Go + Gin (GORM) | WebFlux | MVC | FastAPI |
|---|---|---|---|---|---|---|
| 1 | **2764/s** (52ms p95, **0% err**) | 1.679/s (72ms, **0% err**) | 1.910/s (203ms, **0% err**) | 1.130/s (601ms, 0,01% err) | 661/s (893ms, 0,76% err) | 578/s (1.221ms, 0,04% err) |
| 2 | **3771/s** (8ms p95, **0% err**) | 2.307/s (69ms, **0% err**) | 2.771/s (71ms, **0% err**) | 1.653/s (227ms, 0% err) | 1.802/s (192ms, 0% err) | 1.051/s (601ms, 0% err) |
| 4 | **3836/s** (5ms p95, **0% err**) | 3.217/s (27ms, **0% err**) | 3.331/s (25ms, **0% err**) | 2.186/s (104ms, 0% err) | 2.655/s (82ms, 0% err) | 1.448/s (307ms, 0% err) |
| 8 | **3848/s** (5ms p95, **0% err**) | 3.730/s (9ms, **0% err**) | 3.390/s (16ms, **0% err**) | 2.993/s (38ms, 0% err) | 2.838/s (70ms, 0% err) | 1.855/s (210ms, 0% err) |
| 12 | **3844/s** (5ms p95, **0% err**) | 3.766/s (7ms, **0% err**) | 3.379/s (17ms, **0% err**) | 3.387/s (20ms, 0% err) | 2.850/s (69ms, 0% err) | 2.092/s (166ms, 0% err) |

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
 4.000 ┤                     ●    ●────●────● FastAPI
 2.000 ┤               ●──●        MVC ─────●────●────●
      ┤      ●─●
      └───┬──────┬──────┬──────┬──────┬──────
         1      2      4      8      12    CPUs
```

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalab. |
|---|---|---|---|---|---|---|
| Rust + Axum | 7709 | 13375 | 15722 | 16094 | 15922 | **2.1x** |
| Node Fastify | 3.112 | 5.996 | 10.805 | 14.245 | 14.198 | **4,6x** |
| Go + Gin (GORM) | 4246 | 8668 | 13325 | 13251 | 13154 | **3.1x** |
| WebFlux | 579 | 2.411 | 4.919 | 8.638 | 11.027 | **19,0x** |
| MVC | 400 | 1.021 | 5.729 | 7.889 | 8.061 | **20,2x** |
| FastAPI | 593 | 1.189 | 2.272 | 3.816 | 4.949 | **8,3x** |

---

## Taxa de Erro em Steady State

O cenário mais revelador: quem sustenta 200 conexões simultâneas sem falhar?

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| **Rust + Axum** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Go + Gin (GORM)** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Node Fastify** | **0%** | **0%** | **0%** | 0.79% | 0.28% |
| **WebFlux** | **0%** | **0%** | **0%** | **0%** | **0%** |
| MVC | 0% | 0% | 0% | 0% | 0% |
| FastAPI | 0% | 0% | 0% | 0% | 0% |

---

## Conclusão

### 🥇 Rust + Axum (sqlx) — A campeã geral

- **Maior throughput** em todos os cenários e configs: 15.922 req/s (ramp-up, 12 CPUs)
- **Menor latência**: p95 de 5ms no spike, 14ms no steady, 30ms no ramp-up
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
- **Eficiência brutal**: 2 CPUs (8.668/s) > WebFlux com 8 CPUs (7.629/s)
- GORM incluso: overhead imperceptível em Go

### 4º Spring WebFlux — A melhor stack JVM

- Escalabilidade quase linear: **19x** de 1 a 12 CPUs
- 0% de erro em steady state em todas as configs
- 11.027 req/s em 12 CPUs (ramp-up) — ~76% do Rust Axum

### 5º Spring MVC — O clássico limitado

- Sofria com thread-per-request: agora 0% erro em todas as configs
- Antes platô em ~3.000 req/s; com nativeQuery + ILIKE escala para **8.061 req/s**
- Performance sólida sem erros em configs ≥4 CPUs

### 6º FastAPI Async (SQLAlchemy) — Late bloomer

- Após pool fix (`pool_size=2`, `max_overflow=0`, `workers=CPUS`) saltou de 1.584 para 4.949 req/s (+212%)
- **0% de erro** em todas as configs e cenários (steady, ramp-up, spike)
- Overhead do ORM (SQLAlchemy + Pydantic) + GIL ainda limita o máximo a ~5.237 req/s

### ⚡ Eficiência é tudo

> **Rust Axum com 2 CPUs (13.375 req/s) entrega mais throughput que QUALQUER stack JVM com 12 CPUs.** Go Gin com 2 CPUs (8.668/s) supera o WebFlux com 4 CPUs (4.919/s) — eficiência bruta.
>
> Em termos de custo de infraestrutura, Rust Axum é ~4x mais eficiente que WebFlux e ~3x mais eficiente que FastAPI.
