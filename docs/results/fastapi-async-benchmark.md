# FastAPI Async — Benchmark por Configuração de CPU

> **Stack:** FastAPI + Uvicorn (async) com SQLAlchemy async ORM + Pydantic  
> **Workers:** CPU + 1 (ex: 1 CPU = 2 workers, 12 CPUs = 13 workers)  
> **Banco:** PostgreSQL 16 (Docker), 10.000 usuários  
> **Ferramenta:** k6 — 1 execução por cenário  
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`

---

## Steady State (200 VUs, 30s, sem sleep)

Carga constante e agressiva. Testa se o backend sustenta 200 conexões simultâneas sem acumular backlog.

| Métrica | 1 CPU (2w) | 2 CPUs (3w) | 4 CPUs (5w) | 8 CPUs (9w) | 12 CPUs (13w) |
|---|---|---|---|---|---|
| Throughput (req/s) | 2.500 | 1.798 | 2.478 | 2.287 | 1.529 |
| Total requisições | 77.376 | 54.834 | 75.711 | 69.420 | 46.308 |
| Latência média (ms) | 78,67 | 110,10 | 79,88 | 86,85 | 130,00 |
| Latência p50 (ms) | 16,47 | 18,49 | 18,02 | 19,28 | 99,32 |
| Latência p90 (ms) | 86,67 | 330,27 | 181,43 | 254,68 | 272,34 |
| Latência p95 (ms) | 492,89 | 488,80 | 451,03 | 324,15 | 327,46 |
| Latência máxima (ms) | 5.685,79 | 3.363,21 | 2.457,49 | 2.001,32 | 1.630,19 |
| **Erros** | **87,21%** | **57,10%** | **53,36%** | **43,37%** | **0,00%** |

> **Análise:** Com 1–8 CPUs, o número de workers (2–9) é insuficiente para 200 conexões simultâneas sem sleep — o event loop satura, nginx retorna 502/504. Apenas com 13 workers (12 CPUs) o FastAPI consegue absorver toda a carga sem erros. O throughput bruto é enganoso em lower-CPUs: as requisições com erro são rápidas (nginx rejeita antes de chegar no Python), inflando a contagem.

---

## Ramp-up (0 → 500 VUs, ~80s)

Carga crescente em 5 estágios. Mostra o ponto de degradação de cada config.

| Métrica | 1 CPU (2w) | 2 CPUs (3w) | 4 CPUs (5w) | 8 CPUs (9w) | 12 CPUs (13w) |
|---|---|---|---|---|---|
| Throughput (req/s) | 520 | 1.055 | 1.606 | 1.626 | 1.584 |
| Total requisições | 41.586 | 84.429 | 128.517 | 130.056 | 126.702 |
| Latência média (ms) | 424,50 | 206,35 | 135,03 | 133,36 | 137,08 |
| Latência p50 (ms) | 203,90 | 101,87 | 67,53 | 66,54 | 67,09 |
| Latência p90 (ms) | 1.180,99 | 554,22 | 364,04 | 350,43 | 406,67 |
| Latência p95 (ms) | 1.481,05 | 720,06 | 462,70 | 454,96 | 503,47 |
| Latência máxima (ms) | 8.396,34 | 4.595,43 | 3.202,95 | 2.626,12 | 3.203,15 |
| **Erros** | **~0%** | **~0%** | **~0%** | **~0%** | **~0%** |

> **Análise:** Em ramp-up (carga variável), todas as configs têm erro **< 0,005%** — o backpressure funciona bem quando a carga não é constante. O throughput escala de **520 → 1.606 req/s** (3,1x) de 1 para 4 CPUs, mas **estagna em ~1.600 req/s a partir de 4 CPUs** — o bottleneck muda para o ORM (SQLAlchemy + Pydantic) dentro de cada worker. A latência p95 cai de 1.481ms (1 CPU) para 455ms (8 CPUs), mas sobe levemente em 12 CPUs (503ms).

---

## Spike (50 → 500 → 50 VUs, 75s)

Pico repentino de carga. Testa resiliência e recuperação.

| Métrica | 1 CPU (2w) | 2 CPUs (3w) | 4 CPUs (5w) | 8 CPUs (9w) | 12 CPUs (13w) |
|---|---|---|---|---|---|
| Throughput (req/s) | 454 | 938 | 1.224 | 1.237 | 1.211 |
| Total requisições | 34.071 | 70.374 | 91.956 | 92.904 | 90.846 |
| Latência média (ms) | 276,09 | 113,26 | 77,98 | 76,85 | 79,36 |
| Latência p50 (ms) | 79,14 | 9,55 | 6,27 | 5,98 | 6,23 |
| Latência p90 (ms) | 1.207,31 | 503,99 | 371,24 | 363,17 | 360,01 |
| Latência p95 (ms) | 1.398,12 | 656,54 | 414,06 | 409,51 | 419,73 |
| Latência máxima (ms) | 7.189,59 | 5.665,41 | 2.580,25 | 2.978,66 | 2.483,51 |
| **Erros** | **0,22%** | **0,03%** | **0,00%** | **0,00%** | **0,00%** |

> **Análise:** A partir de **4 CPUs, erro 0%** no spike. A mediana (p50) cai drasticamente de 79ms (1 CPU) para ~6ms (4+ CPUs) — mais workers absorvem o pico de 500 VUs sem fila. O throughput escala 2,7x de 1 para 4 CPUs (454 → 1.224 req/s) e estabiliza.

---

## Comparativo de Escalabilidade

Usando ramp-up (cenário mais estável e sem erros significativos):

| Configuração | Workers | Throughput (req/s) | Escalabilidade | p95 (ms) |
|---|---|---|---|---|
| 1 CPU / 1 GB | 2 | 520 | 1,0x (base) | 1.481 |
| 2 CPUs / 2 GB | 3 | 1.055 | 2,0x | 720 |
| 4 CPUs / 4 GB | 5 | 1.606 | 3,1x | 463 |
| 8 CPUs / 8 GB | 9 | 1.626 | 3,1x | 455 |
| 12 CPUs / 12 GB | 13 | 1.584 | 3,0x | 503 |

### Curva de Throughput (Ramp-up)

```
1.800 ┤
1.600 ┤─────────────────●────●────●
1.400 ┤
1.200 ┤
1.000 ┤────────●
  800 ┤
  600 ┤
  400 ┤──●
  200 ┤
      └───┬─────┬─────┬─────┬─────┬
         1     2     4     8    12  CPUs
```

> O FastAPI escala bem até **4 CPUs (3,1x)**, mas **platôa em ~1.600 req/s** — o overhead do SQLAlchemy ORM + validação Pydantic + GIL dentro de cada worker limita o throughput máximo.

---

## Resumo

| Cenário | Melhor Config | Motivo |
|---|---|---|
| **Steady State** | 12 CPUs (0% erro) | Única config que sustenta 200 conexões sem erros |
| **Ramp-up** | 4–8 CPUs (~1.600 req/s) | Melhor custo-benefício em throughput; 12 CPUs não melhora |
| **Spike** | 4 CPUs+ (0% erro) | A partir de 4 CPUs, absorve pico de 500 VUs sem falhas |

**Conclusão:** Para FastAPI Async com ORM, **4 CPUs / 5 workers** é o ponto ótimo — máximo throughput com 0% de erro em spike e ramp-up. Acima disso, o ganho é marginal (bottleneck no ORM + Pydantic). Para steady state agressivo (200 VUs constantes), são necessários **12 CPUs / 13 workers** para zerar erros, mas com throughput menor que configs inferiores (devido ao processamento completo sem descartes rápidos).
