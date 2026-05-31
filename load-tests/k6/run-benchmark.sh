#!/usr/bin/env bash
set -euo pipefail

K6_DIR="$(cd "$(dirname "$0")" && pwd)"
SCENARIOS_DIR="$K6_DIR/scenarios"
RESULTS_DIR="$K6_DIR/results"
DOCS_DIR="$K6_DIR/../../docs/results"
SCENARIOS=("steady" "ramp-up" "spike")
RUNS=5

mkdir -p "$RESULTS_DIR" "$DOCS_DIR"

echo "=============================================="
echo " Benchmark Spring MVC"
echo " Cenarios: ${SCENARIOS[*]}"
echo " Execucoes por cenario: $RUNS"
echo "=============================================="

for scenario in "${SCENARIOS[@]}"; do
  echo ""
  echo "--- Cenario: $scenario ---"
  for run in $(seq 1 $RUNS); do
    export_file="$RESULTS_DIR/${scenario}-run${run}.json"
    echo "  Run $run/$RUNS..."
    k6 run "$SCENARIOS_DIR/${scenario}.js" \
      --summary-export "$export_file" \
      --quiet 2>/dev/null
    echo "    -> $export_file"
  done
done

echo ""
echo "Calculando medias..."

avg_rows=()
med_rows=()
p90_rows=()
p95_rows=()
tput_rows=()
err_rows=()

for scenario in "${SCENARIOS[@]}"; do
  s_avg=0; s_med=0; s_p90=0; s_p95=0; s_tput=0; s_err=0

  for run in $(seq 1 $RUNS); do
    f="$RESULTS_DIR/${scenario}-run${run}.json"
    s_avg=$(echo "$s_avg + $(jq '.metrics.http_req_duration.avg' "$f")" | bc -l)
    s_med=$(echo "$s_med + $(jq '.metrics.http_req_duration.med' "$f")" | bc -l)
    s_p90=$(echo "$s_p90 + $(jq '.metrics.http_req_duration."p(90)"' "$f")" | bc -l)
    s_p95=$(echo "$s_p95 + $(jq '.metrics.http_req_duration."p(95)"' "$f")" | bc -l)
    s_tput=$(echo "$s_tput + $(jq '.metrics.http_reqs.rate' "$f")" | bc -l)
    s_err=$(echo "$s_err + $(jq '.metrics.http_req_failed.value' "$f")" | bc -l)
  done

  avg_rows+=("$(echo "scale=2; $s_avg / $RUNS" | bc -l)")
  med_rows+=("$(echo "scale=2; $s_med / $RUNS" | bc -l)")
  p90_rows+=("$(echo "scale=2; $s_p90 / $RUNS" | bc -l)")
  p95_rows+=("$(echo "scale=2; $s_p95 / $RUNS" | bc -l)")
  tput_rows+=("$(echo "scale=0; $s_tput / $RUNS" | bc -l)")
  err_rows+=("$(echo "scale=2; $s_err * 100 / $RUNS" | bc -l)")
done

echo ""
echo "Gerando markdown..."

MD_FILE="$DOCS_DIR/spring-mvc-benchmark.md"

{
  echo "# Benchmark Spring MVC (Kotlin)"
  echo ""
  echo "**Data:** $(date '+%d/%m/%Y %H:%M')"
  echo "**Stack:** Spring MVC + Kotlin + JDBC + PostgreSQL"
  echo "**Execucoes por cenario:** $RUNS"
  echo "**Metrica exibida:** media aritmetica das execucoes"
  echo ""
  echo "## Resultados"
  echo ""
  echo "| Metrica | Steady | Ramp-up | Spike |"
  echo "|---|---|---|---|"
  echo "| avg (ms) | ${avg_rows[0]} | ${avg_rows[1]} | ${avg_rows[2]} |"
  echo "| med / p50 (ms) | ${med_rows[0]} | ${med_rows[1]} | ${med_rows[2]} |"
  echo "| p90 (ms) | ${p90_rows[0]} | ${p90_rows[1]} | ${p90_rows[2]} |"
  echo "| p95 (ms) | ${p95_rows[0]} | ${p95_rows[1]} | ${p95_rows[2]} |"
  echo "| throughput (req/s) | ${tput_rows[0]} | ${tput_rows[1]} | ${tput_rows[2]} |"
  echo "| erro (%) | ${err_rows[0]}% | ${err_rows[1]}% | ${err_rows[2]}% |"
} > "$MD_FILE"

echo ""
echo "=============================================="
echo " Benchmark concluido!"
echo " Markdown: $MD_FILE"
echo " JSONs:    $RESULTS_DIR/"
echo "=============================================="
