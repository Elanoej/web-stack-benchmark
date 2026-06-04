#!/usr/bin/env python3
"""Gera relatorio consolidado com curva de escalabilidade entre todas as configs."""
import json, os, sys

base_dir = os.path.join(os.path.dirname(__file__), "../..", "docs", "results")
configs = ["1cpus-1gb", "2cpus", "4cpus-4gb", "8cpus-8gb", "12cpus-12gb"]
config_labels = {
    "1cpus-1gb": "1 CPU / 1GB",
    "2cpus": "2 CPUs / 2GB",
    "4cpus-4gb": "4 CPUs / 4GB",
    "8cpus-8gb": "8 CPUs / 8GB",
    "12cpus-12gb": "12 CPUs / 12GB",
}
stacks = ["spring-mvc", "spring-webflux", "fastapi-async"]
scenarios = ["steady", "ramp-up", "spike"]
scenario_titles = {
    "steady": "Steady State (200 VUs)",
    "ramp-up": "Ramp-up (0→500 VUs)",
    "spike": "Spike (pico 500 VUs)",
}

# Collect data: data[config][stack][scenario] = {tput, p95, err_pct}
data = {}
for cfg in configs:
    data[cfg] = {}
    for stack in stacks:
        data[cfg][stack] = {}
        for sc in scenarios:
            fp = os.path.join(base_dir, cfg, stack, f"{sc}.json")
            if os.path.exists(fp):
                with open(fp) as f:
                    d = json.load(f)
                m = d["metrics"]
                data[cfg][stack][sc] = {
                    "tput": m["http_reqs"]["rate"],
                    "p95": m["http_req_duration"]["p(95)"],
                    "err_pct": m["http_req_failed"].get("value", 0) * 100,
                    "avg": m["http_req_duration"]["avg"],
                    "p50": m["http_req_duration"]["med"],
                    "max": m["http_req_duration"]["max"],
                }

def fmt_tput(v):
    return f"{v:.0f}" if v else "—"

def fmt_ms(v):
    return f"{v:.0f}" if v else "—"

def fmt_pct(v):
    return f"{v:.2f}%" if v else "—"

md = []
md.append("# Benchmarks — Curva de escalabilidade")
md.append("")
md.append("> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.")
md.append("> Todas as stacks limitadas a CPU e RAM via Docker. FastAPI com WORKERS = CPUs + 1.")
md.append("")

# ─── Tabela de Throughput ───────────────────────────────────────
md.append("## Throughput (req/s)")
md.append("")
md.append("| Cenário | Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---|---" + "---|" * len(configs))

for sc in scenarios:
    for stack in stacks:
        cells = [scenario_titles[sc], stack]
        for cfg in configs:
            v = data.get(cfg, {}).get(stack, {}).get(sc, {}).get("tput", 0)
            if v == 0:
                cells.append("—")
            else:
                cells.append(fmt_tput(v))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# ─── Tabela de p95 ──────────────────────────────────────────────
md.append("## Latência p95 (ms)")
md.append("")
md.append("| Cenário | Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---|---" + "---|" * len(configs))

for sc in scenarios:
    for stack in stacks:
        cells = [scenario_titles[sc], stack]
        for cfg in configs:
            v = data.get(cfg, {}).get(stack, {}).get(sc, {}).get("p95", 0)
            if v == 0:
                cells.append("—")
            else:
                cells.append(fmt_ms(v))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# ─── Tabela de Erros ────────────────────────────────────────────
md.append("## Taxa de Erro (%)")
md.append("")
md.append("| Cenário | Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---|---" + "---|" * len(configs))

for sc in scenarios:
    for stack in stacks:
        cells = [scenario_titles[sc], stack]
        for cfg in configs:
            v = data.get(cfg, {}).get(stack, {}).get(sc, {}).get("err_pct", 0)
            cells.append(fmt_pct(v))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# ─── Análise ──────────────────────────────────────────────────
md.append("## Análise")
md.append("")

md.append("### Steady State — Erros em todas as configs")
md.append("")
md.append("O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Com excessão do FastAPI, todas as stacks apresentam erros mesmo com 12 CPUs. Isso ocorre porque:")
md.append("- **Spring MVC** (thread-per-request): 200 conexões simultâneas exigem 200 threads do pool. Com CPU limitada, threads competem e o backlog de conexões estoura no nginx")
md.append("- **Spring WebFlux** (reativo): melhora progressivamente com mais CPUs, mas ainda tem ~5% de erro em 12 CPUs — o overhead do R2DBC + reactive streams sob pressão constante")
md.append("- **FastAPI Async**: **0% de erro a partir de 4 CPUs** — o modelo async I/O + workers = CPUs+1 absorve 200 conexões sem saturar o event loop")

md.append("")
md.append("### Ramp-up e Spike — Todas as stacks estáveis")
md.append("")
md.append("Nestes cenários (carga variável com picos), todas as stacks têm erro < 1% em todas as configs a partir de 1 CPU. O modelo gradual permite que o backpressure funcione corretamente em todas as stacks.")
md.append("")

md.append("### Curva de escalabilidade")
md.append("")
md.append("| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |")
md.append("|---|---|---|---|---|---|---|")

# Identify best throughput for steady state across configs
# For "best scaling" we want to see: 
# At 1c: which has highest tput at steady (even if high errors)
# At 12c: which has highest tput at steady

for stack in stacks:
    cells = [stack]
    # Use ramp-up throughput as it's the most stable scenario
    sc = "ramp-up"
    for cfg in configs:
        v = data.get(cfg, {}).get(stack, {}).get(sc, {}).get("tput", 0)
        cells.append(fmt_tput(v))
    
    # Scaling ratio: last / first
    first = max(data.get(configs[0], {}).get(stack, {}).get(sc, {}).get("tput", 1), 1)
    last = max(data.get(configs[-1], {}).get(stack, {}).get(sc, {}).get("tput", 1), 1)
    ratio = last / first
    cells.append(f"{ratio:.1f}x")
    md.append("| " + " | ".join(cells) + " |")

md.append("")
md.append("### Observações finais")
md.append("")
md.append("1. **Spring MVC** escala linearmente até ~4 CPUs e então estabiliza — o throughput não melhora significativamente de 8 para 12 CPUs, indicando que o bottleneck muda para o banco de dados ou nginx")
md.append("2. **Spring WebFlux** escala melhor que MVC em todos os cenários, com latências significativamente mais baixas. É a stack que mais se beneficia de mais CPUs no ramp-up e spike")
md.append("3. **FastAPI Async** atinge platô cedo (~4 CPUs, ~1.600 req/s) e não escala além disso — o overhead do ORM (SQLAlchemy + Pydantic) e do GIL dentro de cada worker limita o throughput máximo. Porém, é a única stack com **0% de erro em steady state** a partir de 4 CPUs")
md.append("4. A **taxa de erro em steady state** é o indicador mais revelador: FastAPI atinge 0% em 4 CPUs, WebFlux precisa de mais recursos para chegar perto, e MVC mantém ~50% de erro mesmo com 12 CPUs — o modelo thread-per-request simplesmente não foi feito para 200 conexões simultâneas com CPU limitada")
md.append("")

out_path = os.path.join(base_dir, "escalabilidade.md")
with open(out_path, "w") as f:
    f.write("\n".join(md))
print(f"Relatorio consolidado: {out_path}")
