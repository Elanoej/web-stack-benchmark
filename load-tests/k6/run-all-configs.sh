#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$SCRIPT_DIR/run-benchmark-config.sh"
BASE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCS_DIR="$BASE_DIR/docs/results"
STACKS=("spring-mvc" "spring-webflux" "fastapi-async")

# Configs: config_name cpus mem
CONFIGS=(
  "1cpus-1gb  1  1G"
  "4cpus-4gb  4  4G"
  "8cpus-8gb  8  8G"
  "12cpus-12gb 12 12G"
)

echo "=============================================="
echo " Benchmark Runner — Todas as configs"
echo "=============================================="
echo ""
echo "Stacks: ${STACKS[*]}"
echo "Configs:"
for cfg in "${CONFIGS[@]}"; do
  read -r name cpus mem <<< "$cfg"
  echo "  $name  ($cpus CPUs / $mem RAM)"
done
echo ""

# ─── Limpar containers anteriores ──────────────────────────────
cd "$BASE_DIR/infra"
echo ">>> Parando containers legados..."
docker compose down --remove-orphans 2>/dev/null || true
sleep 2

# ─── Rodar cada config × stack ─────────────────────────────────
TOTAL=$(( ${#CONFIGS[@]} * ${#STACKS[@]} ))
CURRENT=0

START_TIME=$(date +%s)

for cfg in "${CONFIGS[@]}"; do
  read -r name cpus mem <<< "$cfg"
  echo ""
  echo "══════════════════════════════════════════════"
  echo " CONFIG: $name ($cpus CPUs / $mem RAM)"
  echo "══════════════════════════════════════════════"

  for stack in "${STACKS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo ""
    echo "─── [$CURRENT/$TOTAL] $stack ───"
    bash "$RUNNER" "$name" "$cpus" "$mem" "$stack"
  done

  # Gerar relatório consolidado desta config
  echo ""
  echo ">>> Gerando relatorio consolidado para $name..."
  python3 "$SCRIPT_DIR/generate-report.py" "$name"
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo ""
echo "=============================================="
echo " Todos os benchmarks concluidos!"
echo " Duracao total: $((DURATION / 60))min $((DURATION % 60))s"
echo " Resultados: $DOCS_DIR/"
echo "=============================================="
