# Resultados — 1cpus-1gb

> **Ambiente:** 1 CPUs, 1GB RAM por container. PostgreSQL via Docker. FastAPI com 2 workers.
> **Ferramenta:** k6 — 1 execução por cenário.
> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.

> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.

---

## Steady State (200 VUs, 30s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 4071 | 147 | 113 | 2500 |
| Latência média (ms) | 48.95 | 1340.29 | 1723.13 | 78.67 |
| Latência p50 (ms) | 64.81 | 1305.85 | 696.26 | 16.47 |
| Latência p90 (ms) | 94.19 | 3019.11 | 4501.22 | 86.67 |
| Latência p95 (ms) | 99.41 | 3631.42 | 6996.94 | 492.89 |
| Latência máxima (ms) | 140 | 5706 | 10296 | 5686 |
| Total requisições | 122457 | 4590 | 3606 | 77376 |
| Erros | 0,00% | 0,00% | 0,00% | 87.21% |

---

## Ramp-up (0 → 500 VUs, 80s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 5394 | 507 | 432 | 520 |
| Latência média (ms) | 39.91 | 431.41 | 510.49 | 424.50 |
| Latência p50 (ms) | 14.35 | 307.21 | 388.68 | 203.90 |
| Latência p90 (ms) | 104.90 | 1082.34 | 1192.62 | 1180.99 |
| Latência p95 (ms) | 116.17 | 1112.80 | 1496.58 | 1481.05 |
| Latência máxima (ms) | 198 | 1385 | 4203 | 8396 |
| Total requisições | 431532 | 40605 | 34584 | 41586 |
| Erros | 0.18% | 0,00% | 0,00% | 0.00% |

---

## Spike (50 → 500 → 50 VUs, 75s)

| Métrica | Go + Gin (GORM) | Spring WebFlux | Spring MVC | FastAPI Async (SQLAlchemy) |
|---|------|---|---|---|
| Throughput (req/s) | 2276 | 1135 | 752 | 454 |
| Latência média (ms) | 26.04 | 87.37 | 150.69 | 276.09 |
| Latência p50 (ms) | 1.73 | 1.79 | 17.50 | 79.14 |
| Latência p90 (ms) | 92.61 | 499.79 | 510.30 | 1207.31 |
| Latência p95 (ms) | 95.90 | 614.28 | 712.11 | 1398.12 |
| Latência máxima (ms) | 164 | 779 | 3000 | 7190 |
| Total requisições | 170877 | 85182 | 56448 | 34071 |
| Erros | 0,00% | 0.20% | 0.83% | 0.22% |

---

## Pódio por cenário

| Cenário | 1º | 2º | 3º | 4º |
|---|---|---|---|---|
| Steady State | Go + Gin (GORM) (4071 req/s) | FastAPI Async (SQLAlchemy) (2500 req/s) | Spring WebFlux (147 req/s) | Spring MVC (113 req/s) |
| Ramp-up | Go + Gin (GORM) (5394 req/s) | FastAPI Async (SQLAlchemy) (520 req/s) | Spring WebFlux (507 req/s) | Spring MVC (432 req/s) |
| Spike | Go + Gin (GORM) (2276 req/s) | Spring WebFlux (1135 req/s) | Spring MVC (752 req/s) | FastAPI Async (SQLAlchemy) (454 req/s) |

## Observações

- **Go + Gin (GORM)** teve o maior throughput geral em 1cpus-1gb.
- Em **Steady State (200 VUs, 30s)**: melhor throughput = **Go + Gin (GORM)** (4071 req/s), menor p95 = **Go + Gin (GORM)** (99.41 ms)
- Em **Ramp-up (0 → 500 VUs, 80s)**: melhor throughput = **Go + Gin (GORM)** (5394 req/s), menor p95 = **Go + Gin (GORM)** (116.17 ms)
- Em **Spike (50 → 500 → 50 VUs, 75s)**: melhor throughput = **Go + Gin (GORM)** (2276 req/s), menor p95 = **Go + Gin (GORM)** (95.90 ms)
