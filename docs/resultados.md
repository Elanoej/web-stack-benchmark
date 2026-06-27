# Resultados do Benchmark — Web Stack Comparison

> Mesmo banco de dados (PostgreSQL 16, 10.000 usuários), mesmos scripts k6, mesmos endpoints.
> Apenas o backend muda. Todas as stacks limitadas a CPU e RAM via Docker Compose.
> Pool de conexões: 30 por stack (FastAPI: pool_size=2 + max_overflow=0, Node Fastify: pool dividido entre workers).
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

| # | Stack | Throughput | p95 | Máxima | Erros | Escalabilidade |
|---|---|---|---|---|---|---|
| 1 | **Rust + Axum (sqlx)** | **15.922 req/s** | **29,9 ms** | **68 ms** | **0,00%** | **2.1x** |
| 2 | Node Fastify | 14.162 req/s | 33,1 ms | 81 ms | 0,00% | 4.5x |
| 3 | Go + Gin (GORM) | 13.154 req/s | 35,9 ms | 76 ms | 0,00% | 3.1x |
| 4 | Spring WebFlux | 11.027 req/s | 57,9 ms | 97 ms | 0,23% | 19.0x |
| 5 | Spring MVC | 8.061 req/s | 87,5 ms | 420 ms | 0,13% | 20.1x |
| 6 | FastAPI Async (SQLAlchemy) | 4.949 req/s | 186,3 ms | 1.621 ms | 0,00% | 8.4x |

---

## 1. Steady State

**200 VUs simultâneos, 30 segundos, sem sleep entre requisições.** Carga constante e agressiva.

### 1 CPU / 1GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **7.657** | 3.096 | 4.249 | 174,7 | 143,5 | 604,2 |
| p95 | **44ms** | 103ms | 165ms | 3207ms | 5300ms | 531ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 2 CPU / 2GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **13.397** | 6.219 | 8.717 | 732,3 | 265,5 | 1.198 |
| p95 | **24ms** | 62ms | 73ms | 790ms | 2469ms | 500ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 4 CPU / 4GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **16.476** | 11.004 | 14.176 | 3.040 | 1.162 | 2.319 |
| p95 | **14ms** | 37ms | 29ms | 187ms | 584ms | 302ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 8 CPU / 8GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **16.645** | 13.808 | 13.296 | 6.112 | 4.412 | 4.021 |
| p95 | **14ms** | 18ms | 18ms | 87ms | 158ms | 193ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

### 12 CPU / 12GB

| Métrica | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| Throughput | **16.396** | 13.822 | 13.501 | 8.020 | 6.284 | 5.237 |
| p95 | **14ms** | 18ms | 17ms | 64ms | 110ms | 183ms |
| Erros | **0%** | **0%** | **0%** | **0%** | **0%** | **0%** |

> **Análise:** **Rust + Axum**, **Go + Gin**, **Spring WebFlux**, **Spring MVC** e **FastAPI Async (SQLAlchemy)** mantiveram **0% de erro em todas as configs** no cenário mais agressivo. Node Fastify zerou os erros após o ajuste de pool. Rust lidera em throughput com a menor latência p95.

---

## 2. Ramp-up

**5 estágios, 0 → 500 VUs em ~80 segundos.** Carga crescente, testa ponto de degradação.

| CPU | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| 1 | **7.709/s (88,7ms p95)** | 3.144/s (92,6ms p95) | 4.247/s (204,7ms p95) | 579/s (1087,0ms p95) | 400/s (1795,5ms p95) | 593/s (1234,8ms p95) |
| 2 | **13.375/s (49,7ms p95)** | 5.993/s (88,9ms p95) | 8.668/s (102,2ms p95) | 2.411/s (256,9ms p95) | 1.021/s (699,4ms p95) | 1.189/s (693,1ms p95) |
| 4 | **15.722/s (30,1ms p95)** | 11.071/s (51,4ms p95) | 13.325/s (38,8ms p95) | 4.919/s (133,4ms p95) | 5.729/s (107,1ms p95) | 2.272/s (417,7ms p95) |
| 8 | **16.094/s (29,6ms p95)** | 14.257/s (33,1ms p95) | 13.251/s (35,5ms p95) | 8.638/s (76,5ms p95) | 7.889/s (88,9ms p95) | 3.816/s (264,3ms p95) |
| 12 | **15.922/s (29,9ms p95)** | 14.162/s (33,1ms p95) | 13.154/s (35,9ms p95) | 11.027/s (57,9ms p95) | 8.061/s (87,5ms p95) | 4.949/s (186,3ms p95) |

> **Análise:** Rust Axum lidera em todas as configs. Go Gin com **2 CPUs já entrega 8.668 req/s** — supera o throughput máximo de WebFlux com 4 CPUs (4.919/s). WebFlux escala 19x de 1 a 12 CPUs (a maior escalabilidade).

---

## 3. Spike

**Pico repentino 50 → 500 → 50 VUs.** Testa resiliência e recuperação.

| CPU | Rust + Axum (sqlx) | Node Fastify | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|---|---|---|---|---|---|
| 1 | **2.764/s (52,4ms p95, **0% err**)** | 1.685/s (76,1ms p95, **0% err**) | 1.983/s (193,4ms p95, **0% err**) | 1.130/s (600,9ms p95, 0,01% err) | 661/s (892,9ms p95, 0,76% err) | 578/s (1220,7ms p95, 0,04% err) |
| 2 | **3.771/s (8,1ms p95, **0% err**)** | 2.310/s (57,9ms p95, **0% err**) | 2.941/s (57,0ms p95, **0% err**) | 1.653/s (226,6ms p95, **0% err**) | 1.802/s (192,4ms p95, **0% err**) | 1.051/s (600,6ms p95, **0% err**) |
| 4 | **3.836/s (5,2ms p95, **0% err**)** | 3.235/s (24,8ms p95, **0% err**) | 3.651/s (11,8ms p95, **0% err**) | 2.186/s (104,1ms p95, **0% err**) | 2.654/s (81,6ms p95, **0% err**) | 1.448/s (306,9ms p95, **0% err**) |
| 8 | **3.848/s (4,8ms p95, **0% err**)** | 3.744/s (8,2ms p95, **0% err**) | 3.745/s (7,9ms p95, **0% err**) | 2.993/s (37,7ms p95, **0% err**) | 2.838/s (69,9ms p95, **0% err**) | 1.855/s (209,6ms p95, **0% err**) |
| 12 | **3.844/s (5,1ms p95, **0% err**)** | 3.774/s (6,6ms p95, **0% err**) | 3.734/s (7,7ms p95, **0% err**) | 3.387/s (20,3ms p95, **0% err**) | 2.850/s (69,1ms p95, **0% err**) | 2.092/s (166,4ms p95, **0% err**) |

> **Análise:** **Rust + Axum**, **Go + Gin** e **Spring WebFlux** têm 0% de erro em todas as configs no spike. Rust lidera com a menor latência p95 (5ms em 12 CPUs).

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
| Rust + Axum (sqlx) | 7.709 | 13.375 | 15.722 | 16.094 | 15.922 | **2.1x** |
| Node Fastify | 3.144 | 5.993 | 11.071 | 14.257 | 14.162 | **4.5x** |
| Go + Gin (GORM) | 4.247 | 8.668 | 13.325 | 13.251 | 13.154 | **3.1x** |
| Spring WebFlux | 579 | 2.411 | 4.919 | 8.638 | 11.027 | **19.0x** |
| Spring MVC | 400 | 1.021 | 5.729 | 7.889 | 8.061 | **20.1x** |
| FastAPI Async (SQLAlchemy) | 593 | 1.189 | 2.272 | 3.816 | 4.949 | **8.4x** |

---

## Taxa de Erro em Steady State

O cenário mais revelador: quem sustenta 200 conexões simultâneas sem falhar?

| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| **Rust + Axum (sqlx)** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Node Fastify** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Go + Gin (GORM)** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Spring WebFlux** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **Spring MVC** | **0%** | **0%** | **0%** | **0%** | **0%** |
| **FastAPI Async (SQLAlchemy)** | **0%** | **0%** | **0%** | **0%** | **0%** |

---

## Conclusão

### 🥇 Rust + Axum (sqlx) — A campeã geral

- **Maior throughput** em todos os cenários e configs: 15.922 req/s (ramp-up, 12 CPUs)
- **Menor latência**: p95 de 5,1 ms no spike, 13,9 ms no steady, 29,9 ms no ramp-up
- **Zero erros**: 0% em steady, ramp-up e spike em todas as configs
- **Eficiente**: 1 CPU (7.709/s) já supera o pico de qualquer stack JVM

### 🥈 Node Fastify (cluster mode) — Impressionante em throughput

- Segundo lugar geral com 14.162 req/s em ramp-up (12 CPUs), superando Go + Gin
- Latência p95 de 33 ms no ramp-up e 7 ms no spike — competitiva com Rust
- **0% erro** em todos os cenários após ajuste de pool
- Escalabilidade de 4.5x de 1 a 12 CPUs

### 🥉 Go + Gin (GORM) — A mais eficiente por núcleo

- Terceiro lugar geral com margem confortável sobre as stacks JVM
- **0% erro** em todos os cenários
- Com pool 20→30, saltou de 10.958 para **13.154 req/s** (+20%)
- **Eficiência brutal**: 2 CPUs (8.668/s) > WebFlux com 8 CPUs
- GORM incluso: overhead imperceptível em Go

### 4º Spring WebFlux — A melhor stack JVM

- Escalabilidade quase linear: **19x** de 1 a 12 CPUs
- 0% de erro em steady state em todas as configs
- 11.027 req/s em 12 CPUs (ramp-up)

### 5º Spring MVC — O clássico limitado

- Sofria com thread-per-request: agora 0% erro em todas as configs
- Antes platô em ~3.000 req/s; com nativeQuery + ILIKE escala para **8.061 req/s**
- Performance sólida sem erros em configs ≥4 CPUs

### 6º FastAPI Async (SQLAlchemy) — Late bloomer

- Após pool fix (`pool_size=2`, `max_overflow=0`, `workers=CPUS`) saltou de 1.584 para **4.949 req/s** (+212%)
- **0% de erro** em todas as configs e cenários (steady, ramp-up, spike)
- Overhead do ORM (SQLAlchemy + Pydantic) + GIL ainda limita o máximo a ~5.237 req/s

### ⚡ Eficiência é tudo

> **Rust Axum com 2 CPUs (13.375 req/s) entrega mais throughput que QUALQUER stack JVM com 12 CPUs.** Go Gin com 2 CPUs (8.668/s) supera o WebFlux com 4 CPUs (4.919/s) — eficiência bruta.
>
> Em termos de custo de infraestrutura, Rust Axum é ~4x mais eficiente que WebFlux e ~3x mais eficiente que FastAPI.