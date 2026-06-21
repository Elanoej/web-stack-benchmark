# =============================================================
# Estágio 1 — chef
# Imagem base com cargo-chef instalado.
# cargo-chef resolve o problema de cache de dependências:
# compila só as deps primeiro, e só recompila o código fonte
# quando o src/ muda — não as deps.
# =============================================================
FROM lukemathwalker/cargo-chef:latest-rust-1.96.0 AS chef
WORKDIR /app

# =============================================================
# Estágio 2 — planner
# Analisa o projeto e gera um "recipe" — um snapshot das
# dependências necessárias, sem o código fonte.
# =============================================================
FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# =============================================================
# Estágio 3 — builder
# Compila as dependências usando o recipe (camada cacheável),
# depois copia o código e compila o binário final.
# =============================================================
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json

COPY . .
RUN cargo build --release --bin rust-axum

# =============================================================
# Estágio 4 — runtime
# Imagem mínima — só o binário e as libs do sistema.
# Resultado final ~100MB vs ~2GB do estágio de build.
# =============================================================
FROM debian:bookworm-slim AS runtime

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Usuário não-root — boa prática de segurança em containers
RUN useradd -u 1001 -m appuser

WORKDIR /app

COPY --from=builder /app/target/release/rust-axum .

EXPOSE 8080

USER appuser

ENTRYPOINT ["./rust-axum"]