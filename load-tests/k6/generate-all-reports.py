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
stacks = ["go-gin", "spring-webflux", "spring-mvc", "fastapi-async"]
stack_labels = {
    "go-gin": "Go + Gin (GORM)",
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
    md.append(f"> **Ambiente:** {cpu_num} CPUs, {mem_label} RAM por container. PostgreSQL via Docker.{workers_note}")
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
md.append("> Todas as stacks limitadas a CPU e RAM via Docker. FastAPI com WORKERS = CPUs + 1.")
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
md.append("- **Go + Gin (GORM)**: **0% de erro em todas as configs** — a única stack que conseguiu. Mesmo com 1 CPU, sustenta 4.071 req/s sem uma única falha.")
md.append("- **Spring WebFlux**: também 0% de erro em todas as configs, mas com throughput 50-55% menor que Go Gin.")
md.append("- **Spring MVC**: 68% de erro em 2 CPUs — o pool de threads do modelo thread-per-request não sustenta 200 conexões simultâneas. A partir de 4 CPUs o erro zera, mas o throughput é 5x menor que Go Gin.")
md.append("- **FastAPI Async (SQLAlchemy + Pydantic)**: 87% de erro em 1 CPU, melhorando progressivamente até zerar em 12 CPUs. O overhead do ORM (SQLAlchemy + Pydantic) associado ao GIL satura o event loop com poucos workers.")
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
md.append("1. **Go + Gin (GORM)** domina todos os cenários: maior throughput, menor latência, **zero erros em todos os testes**. A combinação de runtime compilado (Go), modelo concorrente (goroutines) e framework eficiente (Gin) com GORM entrega 2x o throughput do WebFlux com latência 50% menor — mesmo utilizando um ORM completo.")
md.append("2. **Spring WebFlux** é a melhor stack JVM, com escalabilidade quase linear (19x de 1 para 12 CPUs em ramp-up) e 0% de erro em steady state em todas as configs. Porém, seu throughput máximo é ~50% do Go Gin.")
md.append("3. **Spring MVC** sofre com o modelo thread-per-request: 68% de erro em 2 CPUs no steady state. Escala bem até 4 CPUs (7,1x) e então platôa — o bottleneck muda para o banco ou nginx.")
md.append("4. **FastAPI Async (SQLAlchemy + Pydantic)** é a stack mais fraca em throughput bruto. O overhead do ORM + validação + GIL limita o máximo a ~1.600 req/s. Porém, é a única stack que zera erros em steady state a partir de 4 CPUs (ao lado de Go e WebFlux).")
md.append("5. **A eficiência importa**: Go Gin (GORM) com **2 CPUs** (10.839 req/s) entrega mais throughput que qualquer stack concorrente com **12 CPUs**. Isso tem impacto direto em custo de infraestrutura em produção.")
md.append("")

out_path = os.path.join(base_dir, "escalabilidade.md")
with open(out_path, "w") as f:
    f.write("\n".join(md))
print(f"  Relatorio: {out_path}")

print("\nTodos os relatorios gerados!")
