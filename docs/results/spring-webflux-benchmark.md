# Spring WebFlux — Benchmark por Configuração de CPU

> **Stack:** Spring WebFlux (Kotlin) — reativo/non-blocking, R2DBC, Coroutines  
> **Banco:** PostgreSQL 16 (Docker), 10.000 usuários  
> **Ferramenta:** k6 — 1 execução por cenário  
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`

---

## Steady State (200 VUs, 30s, sem sleep)

Carga constante e agressiva. Testa se o backend sustenta 200 conexões simultâneas sem acumular backlog.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 147 | 669 | 1.932 | 4.235 | **6.507** |
| Total requisições | 4.590 | 20.319 | 58.137 | 127.269 | 195.453 |
| Latência média (ms) | 1.340,29 | 297,73 | 103,29 | 47,07 | 30,60 |
| Latência p50 (ms) | 1.305,85 | 294,83 | 103,18 | 40,13 | 29,88 |
| Latência p90 (ms) | 3.019,11 | 590,42 | 183,86 | 92,96 | 58,39 |
| Latência p95 (ms) | 3.631,42 | 896,03 | 226,25 | 103,94 | **71,46** |
| Latência máxima (ms) | 5.705,68 | 2.684,53 | 1.617,57 | 1.141,27 | 910,37 |
| **Erros** | **0,00%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

> **Análise:** **0% de erro em todas as configs** — o modelo reativo com R2DBC não bloqueia threads mesmo sob 200 conexões simultâneas. O throughput escala de 147/s (1 CPU) para **6.507/s (12 CPUs) — 44,3x de ganho**. A latência p95 cai de 3.631ms para 71ms. Nenhuma outra stack conseguiu 0% de erro em steady state em todas as configurações.

---

## Ramp-up (0 → 500 VUs, ~80s)

Carga crescente em 5 estágios. Mostra o ponto de degradação de cada config.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 507 | 2.094 | 4.746 | 7.629 | **9.641** |
| Total requisições | 40.605 | 167.520 | 379.689 | 610.350 | 771.336 |
| Latência média (ms) | 431,41 | 103,14 | 45,39 | 28,17 | 22,25 |
| Latência p50 (ms) | 307,21 | 102,65 | 29,05 | 18,02 | 14,12 |
| Latência p90 (ms) | 1.082,34 | 226,60 | 126,36 | 78,25 | 59,17 |
| Latência p95 (ms) | 1.112,80 | 267,44 | 141,47 | 87,67 | **67,99** |
| Latência máxima (ms) | 1.384,99 | 361,81 | 171,23 | 134,48 | 109,09 |
| **Erros** | **0,00%** | **0,00%** | **~0%** | **0,12%** | **0,23%** |

> **Análise:** Escalabilidade quase linear — 507 → 9.641 req/s (**19x** de 1 para 12 CPUs). É a única stack que continua escalando significativamente acima de 4 CPUs. A taxa de erro sobe levemente em 8-12 CPUs (0,12-0,23%), possivelmente devido ao backpressure reativo no limite do throughput. A latência p95 em 12 CPUs é de apenas **68ms** — 3x menor que o melhor do MVC (185ms).

---

## Spike (50 → 500 → 50 VUs, 75s)

Pico repentino de carga. Testa resiliência e recuperação.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 1.135 | 1.631 | 2.137 | 2.792 | **3.171** |
| Total requisições | 85.182 | 122.370 | 160.338 | 209.427 | 237.909 |
| Latência média (ms) | 87,37 | 49,85 | 29,94 | 15,02 | 9,20 |
| Latência p50 (ms) | 1,79 | 1,62 | 1,69 | 1,88 | 2,24 |
| Latência p90 (ms) | 499,79 | 211,60 | 105,59 | 46,02 | 25,91 |
| Latência p95 (ms) | 614,28 | 223,21 | 110,80 | 49,11 | **28,36** |
| Latência máxima (ms) | 778,76 | 284,53 | 134,13 | 80,50 | 40,42 |
| **Erros** | **0,20%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

> **Análise:** A partir de 2 CPUs, **0% de erro** no pico de 500 VUs. A latência em 12 CPUs é extraordinária: p50 de **2,2ms**, p95 de **28ms**, máxima de **40ms**. O modelo reativo absorve o spike sem degradação mensurável. Comparado ao MVC (p95 166ms) e FastAPI (p95 420ms), o WebFlux entrega 6-15x menos latência no pico.

---

## Comparativo de Escalabilidade

Usando ramp-up (cenário mais estável):

| Configuração | Throughput (req/s) | Escalabilidade | p95 (ms) |
|---|---|---|---|
| 1 CPU / 1 GB | 507 | 1,0x (base) | 1.113 |
| 2 CPUs / 2 GB | 2.094 | 4,1x | 267 |
| 4 CPUs / 4 GB | 4.746 | 9,4x | 141 |
| 8 CPUs / 8 GB | 7.629 | 15,0x | 88 |
| 12 CPUs / 12 GB | **9.641** | **19,0x** | **68** |

### Curva de Throughput (Ramp-up)

```
10.000 ┤
 9.000 ┤                                        ●
 8.000 ┤
 7.000 ┤                              ●
 6.000 ┤
 5.000 ┤                    ●
 4.000 ┤
 3.000 ┤
 2.000 ┤          ●
 1.000 ┤
       ┤──●
       └───┬─────┬─────┬─────┬─────┬
          1     2     4     8    12  CPUs
```

> **Quase linear:** diferente de MVC e FastAPI (que platoon em 4 CPUs), o WebFlux continua escalando até 12 CPUs — 19x de ganho. A curva ainda não achatou, sugerindo que mais CPUs continuariam trazendo ganho.

---

## Comparação: Steady State (todas as stacks, 12 CPUs)

| Stack | Throughput | p95 | Erros |
|---|---|---|---|
| **Spring WebFlux** | **6.507/s** | **71ms** | **0%** |
| Spring MVC | 2.580/s | 218ms | 0% |
| FastAPI Async | 1.529/s | 327ms | 0% |

## Comparação: Ramp-up (todas as stacks, 12 CPUs)

| Stack | Throughput | p95 | Erros | Escalab. (1→12) |
|---|---|---|---|---|
| **Spring WebFlux** | **9.641/s** | **68ms** | 0,23% | **19,0x** |
| Spring MVC | 3.046/s | 185ms | ~0% | 7,1x |
| FastAPI Async | 1.584/s | 503ms | ~0% | 3,0x |

---

## Resumo

| Cenário | Melhor Config | Motivo |
|---|---|---|
| **Steady State** | 12 CPUs (6.507/s) | 0% erro em todas as configs; escala 44x |
| **Ramp-up** | 12 CPUs (9.641/s) | Escala 19x; única stack sem platô |
| **Spike** | 12 CPUs (3.171/s, p95 28ms) | 0% erro; latência excepcional |

**Conclusão:** O Spring WebFlux é **superior em todos os cenários** — maior throughput, menor latência, 0% de erro em steady state em todas as configs (feito que nenhuma outra stack alcançou). É a única stack que **continua escalando** além de 4 CPUs, indicando que o modelo reativo com R2DBC consegue aproveitar recursos adicionais de forma quase linear. Se o objetivo é performance bruta, WebFlux é a escolha clara.
