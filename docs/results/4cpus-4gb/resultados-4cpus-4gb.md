# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. FastAPI com 5 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 12923 | 1932 | 1421 | 2478 |
| Latência média (ms) | 15.38 | 103.29 | 140.14 | 79.88 |
| Latência p50 (ms) | 15.17 | 103.18 | 114.01 | 18.02 |
| Latência p90 (ms) | 16.99 | 183.86 | 309.13 | 181.43 |
| Latência p95 (ms) | 17.76 | 226.25 | 432.23 | 451.03 |
| Latência máxima (ms) | 578 | 1618 | 3118 | 2457 |
| Total requisições | 388077 | 58137 | 42912 | 75711 |
| Erros | 0,00% | 0,00% | 0,00% | 53.36% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 12305 | 4746 | 3047 | 1606 |
| Latência média (ms) | 17.43 | 45.39 | 70.80 | 135.03 |
| Latência p50 (ms) | 14.95 | 29.05 | 56.53 | 67.53 |
| Latência p90 (ms) | 35.24 | 126.36 | 166.38 | 364.04 |
| Latência p95 (ms) | 38.68 | 141.47 | 187.01 | 462.70 |
| Latência máxima (ms) | 79 | 171 | 525 | 3203 |
| Total requisições | 984438 | 379689 | 243798 | 128517 |
| Erros | 0,00% | 0.01% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 3629 | 2137 | 1644 | 1224 |
| Latência média (ms) | 3.85 | 29.94 | 49.14 | 77.98 |
| Latência p50 (ms) | 2.87 | 1.69 | 10.84 | 6.27 |
| Latência p90 (ms) | 8.68 | 105.59 | 156.69 | 371.24 |
| Latência p95 (ms) | 9.89 | 110.80 | 167.69 | 414.06 |
| Latência máxima (ms) | 25 | 134 | 579 | 2580 |
| Total requisições | 272214 | 160338 | 123300 | 91956 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (12923 req/s) | FastAPI Async (2478 req/s) | Spring WebFlux (1932 req/s) | Spring MVC (1421 req/s) |
| Ramp-up | Go + Gin (12305 req/s) | Spring WebFlux (4746 req/s) | Spring MVC (3047 req/s) | FastAPI Async (1606 req/s) |
| Spike | Go + Gin (3629 req/s) | Spring WebFlux (2137 req/s) | Spring MVC (1644 req/s) | FastAPI Async (1224 req/s) |

## Observações

- **Go + Gin** teve o maior throughput geral em 4cpus-4gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin** (12923 req/s), menor p95 = **Go + Gin** (17.76 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin** (12305 req/s), menor p95 = **Go + Gin** (38.68 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin** (3629 req/s), menor p95 = **Go + Gin** (9.89 ms)
