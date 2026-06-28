# Estágio 1 — build
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

COPY build.gradle.kts settings.gradle.kts ./
COPY gradle gradle
COPY gradlew .

RUN ./gradlew dependencies --no-daemon

COPY src src
RUN ./gradlew installDist --no-daemon

# Estágio 2 — runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /app/build/install/ktor .

ENV JAVA_TOOL_OPTIONS="-XX:+UseZGC -XX:MaxRAMPercentage=75.0"

ENTRYPOINT ["bin/ktor"]
