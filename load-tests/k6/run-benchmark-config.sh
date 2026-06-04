#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 4 ]; then
  echo "Uso: $0 <config_name> <cpus> <mem> <stack>"
  echo "Ex:  $0 4cpus-4gb 4 4G spring-webflux"
  exit 1
fi

CONFIG_NAME="$1"
CPUS="$2"
MEM="$3"
STACK="$4"

K6_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$K6_DIR/../.." && pwd)"
INFRA_DIR="$BASE_DIR/infra"
SCENARIOS_DIR="$K6_DIR/scenarios"
RESULTS_DIR="$BASE_DIR/docs/results/$CONFIG_NAME/$STACK"

mkdir -p "$RESULTS_DIR"

case "$STACK" in
  spring-mvc|spring-webflux|go-stdlib) WORKERS_FINAL="" ;;
  fastapi-async|fastapi-gunicorn)      WORKERS_FINAL=$((CPUS + 1)) ;;
  *)
    echo "Stack desconhecida: $STACK"
    exit 1
    ;;
esac

echo "=============================================="
echo " Config: $CONFIG_NAME  |  Stack: $STACK"
echo " CPUs: $CPUS  |  RAM: $MEM  |  Workers: ${WORKERS_FINAL:--}"
echo " Result: $RESULTS_DIR"
echo "=============================================="

cd "$INFRA_DIR"
docker compose --profile "$STACK" down --remove-orphans 2>/dev/null || true

export CPUS="$CPUS"
export MEM_LIMIT="$MEM"
[ -n "$WORKERS_FINAL" ] && export WORKERS="$WORKERS_FINAL"
export BACKEND_HOST="$STACK"

echo ">>> Subindo $STACK..."
docker compose --profile "$STACK" up -d --force-recreate 2>&1 | grep -v "Network\|Volume" || true

echo ">>> Aguardando $STACK ficar saudavel..."
for i in $(seq 1 30); do
  sleep 2
  STATUS=$(docker inspect "benchmark-${STACK}" --format '{{.State.Status}}' 2>/dev/null || echo "missing")
  HEALTH=$(docker inspect "benchmark-${STACK}" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' 2>/dev/null || echo "unknown")
  if [ "$STATUS" = "running" ] && { [ "$HEALTH" = "running" ] || [ "$HEALTH" = "healthy" ]; }; then
    echo "   $STACK pronto!"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "   ERRO: $STACK nao ficou pronto em 60s"
    docker logs "benchmark-${STACK}" 2>&1 | tail -20
    exit 1
  fi
  echo "   status=$STATUS health=$HEALTH... ($i)"
done

sleep 2

echo ">>> Rodando cenarios k6..."
cd "$BASE_DIR"
for scenario in steady ramp-up spike; do
  echo "  $scenario..."
  k6 run "$SCENARIOS_DIR/${scenario}.js" \
    --summary-export "$RESULTS_DIR/${scenario}.json" \
    --quiet 2>/dev/null || true
  echo "    -> $(du -h "$RESULTS_DIR/${scenario}.json" 2>/dev/null | cut -f1 || echo 'ok')"
done

echo ""
echo ">>> $STACK ($CONFIG_NAME) concluido!"
echo "    Resultados: $RESULTS_DIR"
