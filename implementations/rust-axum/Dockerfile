FROM rust:alpine AS builder

RUN apk add --no-cache musl-dev pkgconfig openssl-dev

WORKDIR /app

RUN mkdir src && echo 'fn main() {}' > src/main.rs

COPY Cargo.toml Cargo.lock ./
RUN cargo build --release 2>&1 || true

COPY src src
RUN cargo build --release

FROM alpine:3.19

RUN apk add --no-cache libgcc

WORKDIR /app

COPY --from=builder /app/target/release/rust-axum .

EXPOSE 8080

ENTRYPOINT ["./rust-axum"]
