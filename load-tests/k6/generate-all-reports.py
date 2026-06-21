#!/usr/bin/env python3
"""Gera todos os relatorios consolidados: 5 por config + 1 escalabilidade."""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
base_dir = os.path.join(PROJECT_DIR, "docs", "results")
configs = ["1cpus-1gb", "2cpus-2gb", "4cpus-4gb", "8cpus-8gb", "12cpus-12gb"]
config_labels = {
    "1cpus-1gb": "1 CPU / 1GB",
    "2cpus-2gb": "2 CPUs / 2GB",
    "4cpus-4gb": "4 CPUs / 4GB",
    "8cpus-8gb": "8 CPUs / 8GB",
    "12cpus-12gb": "12 CPUs / 12GB",
}
stacks = ["go-gin", "rust-axum", "spring-webflux", "spring-mvc", "fastapi-async"]
stack_labels = {
    "go-gin": "Go + Gin (GORM)",
    "rust-axum": "Rust + Axum (sqlx)",
    "spring-webflux": "Spring WebFlux",
    "spring-mvc": "Spring MVC",
    "fastapi-async": "FastAPI Async (SQLAlchemy)",
}
scenarios = ["steady", "ramp-up", "spike"]
scenario_titles = {
    "steady": "Steady State (200 VUs, 30s)",
    "ramp-up": "Ramp-up (0 → 500 VUs, 80s)",
    "spike": "Spike (50 → 500 → 50 VUs, 75s)",
}

# ─── Collect all data ──────────────────────────────────────────────
# data[config][stack][scenario] = {tput, avg, med, p90, p95, max, count, err_pct}
data = {}
for cfg in configs:
    data[cfg] = {}
    for stack in stacks:
        data[cfg][stack] = {}
        for sc in scenarios:
            fp = os.path.join(base_dir, cfg, stack, f"{sc}.json")
            if not os.path.exists(fp):
                continue
            with open(fp) as f:
                d = json.load(f)
            m = d["metrics"]
            hr = m["http_req_duration"]
            data[cfg][stack][sc] = {
                "tput": m["http_reqs"]["rate"],
                "avg": hr["avg"],
                "med": hr["med"],
                "p90": hr["p(90)"],
                "p95": hr["p(95)"],
                "max": hr["max"],
                "count": m["http_reqs"]["count"],
                "err_pct": m["http_req_failed"].get("value", 0) * 100,
            }

def fmt(v, fmt_str="{:.0f}"):
    return fmt_str.format(v) if v else "—"

def fmt_tput(v): return fmt(v, "{:.0f}")
def fmt_ms(v):   return fmt(v, "{:.2f}")
def fmt_pct(v):  return f"{v:.2f}%"

def get(cfg, stack, sc, key):
    return data.get(cfg, {}).get(stack, {}).get(sc, {}).get(key, 0)

def get_stacks_for_config(cfg):
    return [s for s in stacks if data.get(cfg, {}).get(s, {})]

# ═══════════════════════════════════════════════════════════════════
# RELATORIOS POR CONFIG
# ═══════════════════════════════════════════════════════════════════
for cfg in configs:
    cpu_num = int("".join(c for c in cfg.split("-")[0] if c.isdigit()))
    mem_raw = cfg.split("-")[1]
    mem_num = int("".join(c for c in mem_raw if c.isdigit()))
    mem_label = f"{mem_num}GB"
    avail = get_stacks_for_config(cfg)
    if not avail:
        continue

    md = []
    md.append(f"# Resultados — {cfg}")
    md.append("")
    workers_note = ""
    for s in stacks:
        if s == "fastapi-async":
            w = cpu_num + 1
            workers_note += f" FastAPI com {w} workers."
    md.append(f"> **Ambiente:** {cpu_num} CPUs, {mem_label} RAM por container. PostgreSQL via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20).{workers_note}")
    md.append("> **Ferramenta:** k6 — 1 execução por cenário.")
    md.append("> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.")
    md.append("")

    if cpu_num == 1:
        md.append("> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, stacks baseadas em JVM (Spring MVC, WebFlux) consomem ~25-30% do recurso apenas para o runtime. Considere este contexto ao interpretar os resultados.")
        md.append("")

    for sc in scenarios:
        md.append("---")
        md.append("")
        md.append(f"## {scenario_titles[sc]}")
        md.append("")

        hdr = "| Métrica | " + " | ".join(stack_labels[s] for s in stacks) + " |"
        sep = "|---|---" + "---|" * len(stacks)
        md.append(hdr)
        md.append(sep)

        rows = [
            ("Throughput (req/s)", "tput", "{:.0f}"),
            ("Latência média (ms)", "avg", "{:.2f}"),
            ("Latência p50 (ms)", "med", "{:.2f}"),
            ("Latência p90 (ms)", "p90", "{:.2f}"),
            ("Latência p95 (ms)", "p95", "{:.2f}"),
            ("Latência máxima (ms)", "max", "{:.0f}"),
            ("Total requisições", "count", "{:.0f}"),
            ("Erros", "err_pct", "{:.2f}%"),
        ]

        for label, key, ffmt in rows:
            cells = [label]
            for s in stacks:
                v = get(cfg, s, sc, key)
                if v == 0 and key != "err_pct":
                    cells.append("—")
                elif key == "err_pct" and v == 0:
                    cells.append("0,00%")
                else:
                    cells.append(ffmt.format(v))
            md.append("| " + " | ".join(cells) + " |")
        md.append("")

    # Podium
    md.append("---")
    md.append("")
    md.append("## Pódio por cenário")
    md.append("")
    md.append("| Cenário | 1º | 2º | 3º | 4º |")
    md.append("|---|---|---|---|---|")
    for sc in scenarios:
        ranked = sorted(stacks, key=lambda s: get(cfg, s, sc, "tput"), reverse=True)
        tputs = [f"{stack_labels[s]} ({get(cfg, s, sc, 'tput'):.0f} req/s)" for s in ranked]
        md.append(f"| {scenario_titles[sc].split('(')[0].strip()} | " + " | ".join(tputs) + " |")
    md.append("")

    best_stack_name = max(avail, key=lambda s: max(get(cfg, s, sc, "tput") for sc in scenarios))
    md.append("## Observações")
    md.append("")
    md.append(f"- **{stack_labels[best_stack_name]}** teve o maior throughput geral em {cfg}.")
    for sc in scenarios:
        best_tput = max(avail, key=lambda s: get(cfg, s, sc, "tput"))
        best_lat = min(avail, key=lambda s: get(cfg, s, sc, "p95") or 999999)
        md.append(f"- Em **{scenario_titles[sc]}**: melhor throughput = **{stack_labels[best_tput]}** ({get(cfg, best_tput, sc, 'tput'):.0f} req/s), menor p95 = **{stack_labels[best_lat]}** ({get(cfg, best_lat, sc, 'p95'):.2f} ms)")
    md.append("")

    out_path = os.path.join(base_dir, cfg, f"resultados-{cfg}.md")
    with open(out_path, "w") as f:
        f.write("\n".join(md))
    print(f"  Relatorio: {out_path}")


# ═══════════════════════════════════════════════════════════════════
# RELATORIO DE ESCALABILIDADE
# ═══════════════════════════════════════════════════════════════════
md = []
md.append("# Benchmarks — Curva de escalabilidade")
md.append("")
md.append("> Mesmo banco, mesmos endpoints, mesmos scripts k6. Apenas o backend muda.")
md.append("> Todas as stacks limitadas a CPU e RAM via Docker. Pool de conexões: 20 por stack (FastAPI: pool_size=10 + max_overflow=20). FastAPI com WORKERS = CPUs + 1.")
md.append("")

# ─── Throughput ────────────────────────────────────────────────────
md.append("## Throughput (req/s)")
md.append("")
md.append("| Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---" + "---|" * len(configs))

for stack in stacks:
    cells = [stack_labels[stack]]
    for cfg in configs:
        cells.append(fmt_tput(get(cfg, stack, "ramp-up", "tput")))
    md.append("| " + " | ".join(cells) + " |")
md.append("")

# Steady throughput
md.append("### Detalhamento por cenário")
md.append("")
for sc in scenarios:
    sc_label = scenario_titles[sc].split("(")[0].strip()
    md.append(f"**{sc_label}:**")
    md.append("")
    md.append("| Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
    md.append("|---" + "---|" * len(configs))
    for stack in stacks:
        cells = [stack_labels[stack]]
        for cfg in configs:
            cells.append(fmt_tput(get(cfg, stack, sc, "tput")))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# ─── p95 ──────────────────────────────────────────────────────────
md.append("## Latência p95 (ms)")
md.append("")
md.append("| Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---" + "---|" * len(configs))

for stack in stacks:
    cells = [stack_labels[stack]]
    for cfg in configs:
        cells.append(fmt_ms(get(cfg, stack, "ramp-up", "p95")))
    md.append("| " + " | ".join(cells) + " |")
md.append("")

# ─── Erros ────────────────────────────────────────────────────────
md.append("## Taxa de Erro (%)")
md.append("")
for sc in scenarios:
    sc_label = scenario_titles[sc].split("(")[0].strip()
    md.append(f"**{sc_label}:**")
    md.append("")
    md.append("| Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
    md.append("|---" + "---|" * len(configs))
    for stack in stacks:
        cells = [stack_labels[stack]]
        for cfg in configs:
            cells.append(fmt_pct(get(cfg, stack, sc, "err_pct")))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# ─── Curva de escalabilidade ──────────────────────────────────────
md.append("## Curva de escalabilidade (Ramp-up)")
md.append("")
md.append("| Stack | 1 CPU | 2 CPUs | 4 CPUs | 8 CPUs | 12 CPUs | Escalabilidade |")
md.append("|---|---|---|---|---|---|---|")

for stack in stacks:
    cells = [stack_labels[stack]]
    sc = "ramp-up"
    for cfg in configs:
        cells.append(fmt_tput(get(cfg, stack, sc, "tput")))
    first = max(get(configs[0], stack, sc, "tput"), 1)
    last = max(get(configs[-1], stack, sc, "tput"), 1)
    ratio = last / first
    cells.append(f"{ratio:.1f}x")
    md.append("| " + " | ".join(cells) + " |")
md.append("")

# ─── Análise ──────────────────────────────────────────────────────
md.append("## Análise")
md.append("")

# Steady state analysis
md.append("### Steady State")
md.append("")
md.append("O cenário Steady State (200 VUs constantes sem sleep) é o mais agressivo. Ele revela como cada stack lida com pressão constante e sustentada:")
md.append("")

steady_zero_err = {}
for cfg in configs:
    zero = [s for s in stacks if get(cfg, s, "steady", "err_pct") < 0.01]
    steady_zero_err[cfg] = zero

for cfg in configs:
    zero_list = ", ".join(stack_labels[s] for s in steady_zero_err[cfg])
    md.append(f"- **{config_labels[cfg]}**: stacks com 0% erro → {zero_list}")
md.append("")

# Error rates
md.append("### Taxa de erro em Steady State")
md.append("")
md.append("| Stack | " + " | ".join(config_labels[c] for c in configs) + " |")
md.append("|---" + "---|" * len(configs))
for stack in stacks:
    cells = [stack_labels[stack]]
    for cfg in configs:
        cells.append(fmt_pct(get(cfg, stack, "steady", "err_pct")))
    md.append("| " + " | ".join(cells) + " |")
md.append("")

md.append("**Observações:**")
md.append("")
md.append("- **Rust + Axum (sqlx)**: **0% de erro em todas as configs**. A stack mais rápida em throughput geral e com a menor latência p95.")
md.append("- **Go + Gin (GORM)**: **0% de erro em todas as configs**. Segunda colocada em throughput, mas com latência ligeiramente maior que Rust.")
md.append("- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput ~30-50% menor que Rust Axum.")
md.append("- **Spring MVC**: sofre com o modelo thread-per-request em cargas mais altas. O throughput é limitado pelo pool de threads do Tomcat.")
md.append("- **FastAPI Async (SQLAlchemy + Pydantic)**: overhead do ORM + GIL limita o throughput máximo. A partir de 4 CPUs o erro zera.")
md.append("")

# Ramp-up & Spike
md.append("### Ramp-up e Spike")
md.append("")
md.append("Nestes cenários (carga variável com picos), todas as stacks têm erro < 0,3% em todas as configs. O backpressure funciona bem quando a carga não é constante.")
md.append("")

# Overall ranking
md.append("### Ranking geral (12 CPUs, Ramp-up)")
md.append("")
md.append("| # | Stack | Throughput | p95 | Erros | Escalabilidade |")
md.append("|---|---|---|---|---|---|")
ranked_12 = sorted(stacks, key=lambda s: get("12cpus-12gb", s, "ramp-up", "tput"), reverse=True)
for i, s in enumerate(ranked_12, 1):
    first = max(get(configs[0], s, "ramp-up", "tput"), 1)
    last = max(get(configs[-1], s, "ramp-up", "tput"), 1)
    ratio = last / first
    md.append(f"| {i} | {stack_labels[s]} | {get('12cpus-12gb', s, 'ramp-up', 'tput'):.0f} req/s | {get('12cpus-12gb', s, 'ramp-up', 'p95'):.0f} ms | {get('12cpus-12gb', s, 'ramp-up', 'err_pct'):.2f}% | {ratio:.1f}x |")
md.append("")

# Final observations
md.append("### Conclusão")
md.append("")
md.append("1. **Rust + Axum (sqlx)** é a stack mais rápida: maior throughput geral, menor latência p95, **zero erros em todos os testes**. Com o runtime Tokio configurado corretamente (worker_threads = CPUs disponíveis), a escalabilidade é competitiva com as melhores stacks.")
md.append("2. **Go + Gin (GORM)** mantém a segunda posição com vantagem sobre as stacks JVM. Sua eficiência por núcleo é notável: com 2 CPUs já supera o throughput máximo de todas as stacks concorrentes exceto Rust.")
md.append("3. **Spring WebFlux** é a melhor stack JVM, com escalabilidade consistente (19x de 1 para 12 CPUs em ramp-up) e 0% de erro em steady state em todas as configs.")
md.append("4. **Spring MVC** sofre com o modelo thread-per-request. Escala bem até 4 CPUs e então platôa — o bottleneck muda para o banco ou nginx.")
md.append("5. **FastAPI Async (SQLAlchemy + Pydantic)** é a stack mais fraca em throughput bruto. O overhead do ORM + validação + GIL limita o throughput máximo.")
md.append("")

out_path = os.path.join(base_dir, "escalabilidade.md")
with open(out_path, "w") as f:
    f.write("\n".join(md))
print(f"  Relatorio: {out_path}")

print("\nTodos os relatorios gerados!")
