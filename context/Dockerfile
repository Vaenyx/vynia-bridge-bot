# ---------- Build stage ----------
FROM rust:1-bookworm AS builder

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release --locked


# ---------- Runtime stage ----------
FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder \
    /app/target/release/vynia-discord-bot \
    /usr/local/bin/vynia-discord-bot

RUN useradd --create-home --uid 10001 botuser

USER botuser

CMD ["vynia-discord-bot"]
