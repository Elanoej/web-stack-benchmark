# Benchmark FastAPI Async

**Data:** 31/05/2026 19:50
**Stack:** FastAPI + SQLAlchemy async + Pydantic + asyncpg + PostgreSQL
**Execucoes por cenario:** 1 (válidação inicial)
**Metrica exibida:** valores da execução

> Stack mais realista: SQLAlchemy ORM + Pydantic nos responses.
> Pool de conexões: 10 fixas, 20 overflow.

## Resultados

| Metrica | Steady | Ramp-up | Spike |
|---|---|---|---|
| avg (ms) | 132.57 | 143.24 | 108.28 |
| med / p50 (ms) | 83.05 | 39.66 | 5.31 |
| p90 (ms) | 198.33 | 204.47 | 193.89 |
| p95 (ms) | 287.54 | 449.34 | 672.50 |
| throughput (req/s) | 1495 | 1560 | 1085 |
| erro (%) | 22.19% | 14.27% | 9.66% |

## Comparativo com asyncpg puro

| Métrica | asyncpg puro | SQLAlchemy + Pydantic | Diferença |
|---|---|---|---|
| Steady throughput | 1.870 req/s | 1.495 req/s | **1.25x mais lento** |
| Steady erro | 0.01% | 22.19% | **erros surgem com ORM** |
| Spike mediana | 2.88ms | 5.31ms | **1.8x mais lento** |
| Spike throughput | 1.219 req/s | 1.085 req/s | **1.1x mais lento** |

O overhead do SQLAlchemy ORM + Pydantic adiciona latência e consumo de CPU, fazendo o event loop do asyncio entrar em contenção com 200 VUs simultâneos — o que gera timeouts no nginx (erros ~502).
