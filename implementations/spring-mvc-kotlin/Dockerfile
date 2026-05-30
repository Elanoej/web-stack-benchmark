# =============================================================
# Build multi-stage — conceito importante
#
# Estágio 1 (builder): imagem com JDK completo + Gradle
# compila o projeto e gera o .jar
#
# Estágio 2 (runtime): imagem só com JRE (sem Gradle, sem SDK)
# copia o .jar do estágio anterior e roda
#
# Resultado: imagem final ~200MB em vez de ~600MB
# O código fonte e as ferramentas de build não vão para produção
# =============================================================

# Estágio 1 — build
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Copia os arquivos de dependência primeiro
# Docker cacheia camada por camada — se o build.gradle.kts
# não mudou, ele reutiliza o cache das dependências
# e não baixa tudo de novo a cada build
COPY build.gradle.kts settings.gradle.kts ./
COPY gradle gradle
COPY gradlew .

RUN ./gradlew dependencies --no-daemon

# Agora copia o código fonte e compila
COPY src src
RUN ./gradlew bootJar --no-daemon

# =============================================================
# Estágio 2 — runtime
# =============================================================
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]