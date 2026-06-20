# Resultados — 4cpus-4gb

> **Ambiente:** 4 CPUs, 4GB RAM por container. PostgreSQL via Docker. FastAPI com 5 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 13306 | 1932 | 1421 | 2478 |
| Latência média (ms) | 14.93 | 103.29 | 140.14 | 79.88 |
| Latência p50 (ms) | 14.72 | 103.18 | 114.01 | 18.02 |
| Latência p90 (ms) | 16.68 | 183.86 | 309.13 | 181.43 |
| Latência p95 (ms) | 17.44 | 226.25 | 432.23 | 451.03 |
| Latência máxima (ms) | 631 | 1618 | 3118 | 2457 |
| Total requisições | 399612 | 58137 | 42912 | 75711 |
| Erros | 0,00% | 0,00% | 0,00% | 53.36% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 12795 | 4746 | 3047 | 1606 |
| Latência média (ms) | 16.75 | 45.39 | 70.80 | 135.03 |
| Latência p50 (ms) | 14.25 | 29.05 | 56.53 | 67.53 |
| Latência p90 (ms) | 34.28 | 126.36 | 166.38 | 364.04 |
| Latência p95 (ms) | 38.02 | 141.47 | 187.01 | 462.70 |
| Latência máxima (ms) | 98 | 171 | 525 | 3203 |
| Total requisições | 1023570 | 379689 | 243798 | 128517 |
| Erros | 0,00% | 0.01% | 0.01% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 3674 | 2137 | 1644 | 1224 |
| Latência média (ms) | 3.37 | 29.94 | 49.14 | 77.98 |
| Latência p50 (ms) | 2.17 | 1.69 | 10.84 | 6.27 |
| Latência p90 (ms) | 7.74 | 105.59 | 156.69 | 371.24 |
| Latência p95 (ms) | 9.24 | 110.80 | 167.69 | 414.06 |
| Latência máxima (ms) | 20 | 134 | 579 | 2580 |
| Total requisições | 275625 | 160338 | 123300 | 91956 |
| Erros | 0,00% | 0,00% | 0,00% | 0,00% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (GORM) (13306 req/s) | FastAPI Async (SQLAlchemy) (2478 req/s) | Spring WebFlux (1932 req/s) | Spring MVC (1421 req/s) |
| Ramp-up | Go + Gin (GORM) (12795 req/s) | Spring WebFlux (4746 req/s) | Spring MVC (3047 req/s) | FastAPI Async (SQLAlchemy) (1606 req/s) |
| Spike | Go + Gin (GORM) (3674 req/s) | Spring WebFlux (2137 req/s) | Spring MVC (1644 req/s) | FastAPI Async (SQLAlchemy) (1224 req/s) |

## Observações

- **Go + Gin (GORM)** teve o maior throughput geral em 4cpus-4gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin (GORM)** (13306 req/s), menor p95 = **Go + Gin (GORM)** (17.44 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin (GORM)** (12795 req/s), menor p95 = **Go + Gin (GORM)** (38.02 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin (GORM)** (3674 req/s), menor p95 = **Go + Gin (GORM)** (9.24 ms)
