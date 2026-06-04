#!/usr/bin/env python3
"""Gera relatorio markdown consolidado para uma config."""
import json, os, sys

config_name = sys.argv[1]
base_dir = os.path.join(os.path.dirname(__file__), "../..", "docs", "results", config_name)
stacks = ["spring-mvc", "spring-webflux", "fastapi-async"]
scenarios = ["steady", "ramp-up", "spike"]

scenario_titles = {
    "steady": "Steady State (200 VUs, 30s)",
    "ramp-up": "Ramp-up (0 → 500 VUs, 80s)",
    "spike": "Spike (50 → 500 → 50 VUs, 75s)",
}

cpus_label = config_name.split("-")[0]

# Collect data
data = {}
available = []
for stack in stacks:
    stack_data = {}
    ok = True
    for sc in scenarios:
        fp = os.path.join(base_dir, stack, f"{sc}.json")
        if not os.path.exists(fp):
            ok = False
            break
        with open(fp) as f:
            d = json.load(f)
        m = d["metrics"]
        hr = m["http_req_duration"]
        hf = m["http_req_failed"]
        hreq = m["http_reqs"]
        stack_data[sc] = {
            "tput": hreq["rate"],
            "avg": hr["avg"],
            "med": hr["med"],
            "p90": hr["p(90)"],
            "p95": hr["p(95)"],
            "max": hr["max"],
            "count": hreq["count"],
            "err_pct": hf.get("value", 0) * 100,
        }
    if ok:
        data[stack] = stack_data
        available.append(stack)

if not available:
    print(f"Nenhum dado encontrado em {base_dir}")
    sys.exit(1)

# Generate markdown
md = []
md.append(f"# Resultados — {config_name}")
md.append("")
md.append(f"> **Ambiente:** {cpus_label} CPUs, {config_name.replace('cpus-', ' ').replace('1gb', '1GB').replace('2gb', '2GB').replace('4gb', '4GB').replace('8gb', '8GB').replace('12gb', '12GB')} RAM por container. PostgreSQL via Docker.")
md.append("> **Ferramenta:** k6 — 1 execução por cenário.")
md.append("> **Endpoints:** `GET /users/hello`, `GET /users?page=0&size=20`, `POST /users/search`.")
md.append("")

if cpus_label == "1":
    md.append("> **⚠️ Ressalva:** Com 1 CPU e 1GB de RAM, a JVM consome ~25-30% do recurso apenas para o runtime antes da aplicação começar. Este cenário tende a beneficiar stacks com menor footprint (Python) e modelos reativos (WebFlux). Considere este contexto ao interpretar os resultados.")
    md.append("")

for sc in scenarios:
    md.append("---")
    md.append("")
    md.append(f"## {scenario_titles[sc]}")
    md.append("")
    hdr = "| Métrica | " + " | ".join(stacks) + " |"
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

    for label, key, fmt in rows:
        cells = [label]
        for s in stacks:
            v = data.get(s, {}).get(sc, {}).get(key, "—")
            if isinstance(v, (int, float)):
                cells.append(fmt.format(v))
            else:
                cells.append(str(v))
        md.append("| " + " | ".join(cells) + " |")
    md.append("")

# Summary
md.append("---")
md.append("")
md.append("## Resumo por cenário")
md.append("")
md.append("| Cenário | 1º | 2º | 3º |")
md.append("|---|---|---|---|")

for sc in scenarios:
    ranked = sorted(stacks, key=lambda s: data.get(s, {}).get(sc, {}).get("tput", 0), reverse=True)
    tputs = [f"{data.get(s, {}).get(sc, {}).get('tput', 0):.0f} req/s" for s in ranked]
    md.append(f"| {scenario_titles[sc].split('(')[0].strip()} | {ranked[0]} ({tputs[0]}) | {ranked[1]} ({tputs[1]}) | {ranked[2]} ({tputs[2]}) |")

md.append("")

# Observations
md.append("## Observações")
md.append("")

# Best throughput overall
best_stack = max(stacks, key=lambda s: max(data.get(s, {}).get(sc, {}).get("tput", 0) for sc in scenarios))
md.append(f"- **{best_stack}** teve o maior throughput geral nesta configuração.")

for sc in scenarios:
    best_lat = min(stacks, key=lambda s: data.get(s, {}).get(sc, {}).get("p95", 999999))
    best_tput = max(stacks, key=lambda s: data.get(s, {}).get(sc, {}).get("tput", 0))
    md.append(f"- Em **{scenario_titles[sc]}**: melhor throughput = **{best_tput}**, menor p95 = **{best_lat}**")

md.append("")

out_path = os.path.join(base_dir, f"resultados-{config_name}.md")
with open(out_path, "w") as f:
    f.write("\n".join(md))

print(f"  Relatorio: {out_path}")
