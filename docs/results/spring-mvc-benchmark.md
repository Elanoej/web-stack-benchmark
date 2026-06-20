# Spring MVC — Benchmark por Configuração de CPU

> **Stack:** Spring MVC (Kotlin) — thread-per-request, JDBC, HikariCP pool (max 20)  
> **Banco:** PostgreSQL 16 (Docker), 10.000 usuários  
> **Ferramenta:** k6 — 1 execução por cenário  
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`

---

## Steady State (200 VUs, 30s, sem sleep)

Carga constante e agressiva. Testa se o backend sustenta 200 conexões simultâneas sem acumular backlog.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 113 | 896 | 1.421 | 2.464 | 2.580 |
| Total requisições | 3.606 | 27.435 | 42.912 | 74.358 | 77.841 |
| Latência média (ms) | 1.723,13 | 220,82 | 140,14 | 80,79 | 77,14 |
| Latência p50 (ms) | 696,26 | 15,59 | 114,01 | 90,23 | 91,27 |
| Latência p90 (ms) | 4.501,22 | 694,66 | 309,13 | 191,14 | 149,45 |
| Latência p95 (ms) | 6.996,94 | 1.205,87 | 432,23 | 218,70 | 218,36 |
| Latência máxima (ms) | 10.296,09 | 10.199,04 | 3.117,98 | 1.571,33 | 1.040,63 |
| **Erros** | **0,00%** | **68,48%** | **0,00%** | **0,00%** | **0,00%** |

> **Análise:** Com 1 CPU o throughput é baixíssimo (113/s) mas sem erros — a JVM mal consegue processar, mas não rejeita. Com 2 CPUs o throughput sobe 8x, porém o pool de threads (HikariCP max 20 + HTTP threads) não sustenta 200 conexões simultâneas, causando 68% de timeout no nginx. A partir de 4 CPUs o erro zera e o throughput escala até 2.580/s em 12 CPUs.

---

## Ramp-up (0 → 500 VUs, ~80s)

Carga crescente em 5 estágios. Mostra o ponto de degradação de cada config.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 432 | 1.185 | 3.047 | 3.062 | 3.046 |
| Total requisições | 34.584 | 94.776 | 243.798 | 244.989 | 243.699 |
| Latência média (ms) | 510,49 | 182,89 | 70,80 | 70,46 | 70,84 |
| Latência p50 (ms) | 388,68 | 132,93 | 56,53 | 55,46 | 57,84 |
| Latência p90 (ms) | 1.192,62 | 394,50 | 166,38 | 166,06 | 165,12 |
| Latência p95 (ms) | 1.496,58 | 510,32 | 187,01 | 189,63 | 185,02 |
| Latência máxima (ms) | 4.203,29 | 2.023,01 | 525,20 | 649,94 | 523,93 |
| **Erros** | **0,00%** | **~0%** | **~0%** | **~0%** | **~0%** |

> **Análise:** Em ramp-up, todas as configs têm erro < 0,01%. O throughput escala fortemente de 1→4 CPUs (432 → 3.047 req/s, **7,1x**), mas **platôa em ~3.050 req/s** a partir de 4 CPUs — adicionar mais CPUs não melhora. O bottleneck muda para o banco de dados ou nginx. A latência p95 cai de 1.497ms (1 CPU) para 187ms (4 CPUs) e estabiliza.

---

## Spike (50 → 500 → 50 VUs, 75s)

Pico repentino de carga. Testa resiliência e recuperação.

| Métrica | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs |
|---|---|---|---|---|---|
| Throughput (req/s) | 752 | 1.659 | 1.644 | 1.643 | 1.644 |
| Total requisições | 56.448 | 124.470 | 123.300 | 123.393 | 123.450 |
| Latência média (ms) | 150,69 | 48,36 | 49,14 | 49,10 | 49,07 |
| Latência p50 (ms) | 17,50 | 10,43 | 10,84 | 10,69 | 10,86 |
| Latência p90 (ms) | 510,30 | 152,88 | 156,69 | 156,69 | 156,47 |
| Latência p95 (ms) | 712,11 | 163,18 | 167,69 | 167,95 | 165,87 |
| Latência máxima (ms) | 3.000,23 | 574,85 | 579,03 | 518,02 | 550,43 |
| **Erros** | **0,83%** | **0,00%** | **0,00%** | **0,00%** | **0,00%** |

> **Análise:** Com 1 CPU, 0,83% de erro durante o pico para 500 VUs. A partir de **2 CPUs, erro 0%** e throughput consistente em ~1.644 req/s — notavelmente estável entre 2 e 12 CPUs. O pico de 500 VUs é absorvido sem degradação adicional acima de 2 CPUs.

---

## Comparativo de Escalabilidade

Usando ramp-up (cenário mais estável e sem erros significativos):

| Configuração | Throughput (req/s) | Escalabilidade | p95 (ms) |
|---|---|---|---|
| 1 CPU / 1 GB | 432 | 1,0x (base) | 1.497 |
| 2 CPUs / 2 GB | 1.185 | 2,7x | 510 |
| 4 CPUs / 4 GB | 3.047 | **7,1x** | 187 |
| 8 CPUs / 8 GB | 3.062 | 7,1x | 190 |
| 12 CPUs / 12 GB | 3.046 | 7,1x | 185 |

### Curva de Throughput (Ramp-up)

```
3.500 ┤
3.000 ┤──────────────────●────●────●
2.500 ┤
2.000 ┤
1.500 ┤
1.000 ┤─────────●
  500 ┤──●
      └───┬─────┬─────┬─────┬─────┬
         1     2     4     8    12  CPUs
```

> O Spring MVC escala bem até **4 CPUs (7,1x)**, mas **platôa em ~3.050 req/s** — o bottleneck muda do pool de threads para o banco de dados (contensão de locks no PostgreSQL) ou para o nginx (keepalive, fila de conexões).

---

## Resumo

| Cenário | Melhor Config | Motivo |
|---|---|---|
| **Steady State** | 4 CPUs+ (0% erro) | 1 CPU é muito lento; 2 CPUs tem 68% de erro; 4 CPUs+ resolve |
| **Ramp-up** | 4 CPUs (~3.047 req/s) | Ponto ótimo — acima disso não ganha throughput |
| **Spike** | 2 CPUs+ (0% erro) | 2 CPUs já absorve pico de 500 VUs sem falhas |

**Conclusão:** Para Spring MVC, **4 CPUs** é o ponto ótimo — máximo throughput com 0% de erro em todos os cenários. Acima de 4 CPUs não há ganho prático: o throughput estabiliza em ~3.050 req/s (ramp-up) e ~1.644 req/s (spike), indicando que o bottleneck é externo à aplicação (banco de dados ou nginx).
