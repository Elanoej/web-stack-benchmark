# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. FastAPI com 2 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 3626 | 147 | 113 | 2500 |
| Latência média (ms) | 54.92 | 1340.29 | 1723.13 | 78.67 |
| Latência p50 (ms) | 73.28 | 1305.85 | 696.26 | 16.47 |
| Latência p90 (ms) | 95.08 | 3019.11 | 4501.22 | 86.67 |
| Latência p95 (ms) | 98.42 | 3631.42 | 6996.94 | 492.89 |
| Latência máxima (ms) | 132 | 5706 | 10296 | 5686 |
| Total requisições | 109260 | 4590 | 3606 | 77376 |
| Erros | 0,00% | 0,00% | 0,00% | 87.21% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 5375 | 507 | 432 | 520 |
| Latência média (ms) | 40.05 | 431.41 | 510.49 | 424.50 |
| Latência p50 (ms) | 15.19 | 307.21 | 388.68 | 203.90 |
| Latência p90 (ms) | 104.81 | 1082.34 | 1192.62 | 1180.99 |
| Latência p95 (ms) | 112.58 | 1112.80 | 1496.58 | 1481.05 |
| Latência máxima (ms) | 189 | 1385 | 4203 | 8396 |
| Total requisições | 430038 | 40605 | 34584 | 41586 |
| Erros | 0.09% | 0,00% | 0,00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin | Spring WebFlux | Spring MVC | FastAPI Async |
|---|------|---|---|---|
| Throughput (req/s) | 2289 | 1135 | 752 | 454 |
| Latência média (ms) | 25.72 | 87.37 | 150.69 | 276.09 |
| Latência p50 (ms) | 1.79 | 1.79 | 17.50 | 79.14 |
| Latência p90 (ms) | 91.87 | 499.79 | 510.30 | 1207.31 |
| Latência p95 (ms) | 95.14 | 614.28 | 712.11 | 1398.12 |
| Latência máxima (ms) | 159 | 779 | 3000 | 7190 |
| Total requisições | 171750 | 85182 | 56448 | 34071 |
| Erros | 0,00% | 0.20% | 0.83% | 0.22% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (3626 req/s) | FastAPI Async (2500 req/s) | Spring WebFlux (147 req/s) | Spring MVC (113 req/s) |
| Ramp-up | Go + Gin (5375 req/s) | FastAPI Async (520 req/s) | Spring WebFlux (507 req/s) | Spring MVC (432 req/s) |
| Spike | Go + Gin (2289 req/s) | Spring WebFlux (1135 req/s) | Spring MVC (752 req/s) | FastAPI Async (454 req/s) |

## Observações

- **Go + Gin** teve o maior throughput geral em 1cpus-1gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin** (3626 req/s), menor p95 = **Go + Gin** (98.42 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin** (5375 req/s), menor p95 = **Go + Gin** (112.58 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin** (2289 req/s), menor p95 = **Go + Gin** (95.14 ms)
