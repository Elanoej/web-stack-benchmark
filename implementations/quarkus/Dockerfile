FROM maven:3.9.6-eclipse-temurin-21 AS builder

WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN mvn -B -DskipTests package -Dquarkus.package.jar.type=uber-jar

FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /app/target/quarkus-1.0.0-SNAPSHOT-runner.jar /app/quarkus-runner.jar

EXPOSE 5000

ENV QUARKUS_HTTP_PORT=5000
ENV QUARKUS_HTTP_HOST=0.0.0.0

CMD ["java", "-jar", "quarkus-runner.jar"]