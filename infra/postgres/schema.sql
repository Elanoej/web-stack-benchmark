-- =============================================================
-- SCHEMA — web-stack-benchmark
-- =============================================================
-- Rodado automaticamente quando o container do Postgres sobe
-- pela primeira vez (via volume no docker-compose).
-- =============================================================

-- Extensão para gerar UUIDs nativamente no Postgres
-- Em vez de deixar a aplicação gerar o ID, o banco faz isso.
-- Vantagem: menos round-trips, IDs garantidamente únicos.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -------------------------------------------------------------
-- Tabela: users
-- -------------------------------------------------------------
-- Representa um usuário simples. Usada nos endpoints:
--   GET /users          → lista paginada
--   POST /users/search  → busca por nome/cidade
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    city       VARCHAR(100) NOT NULL,
    country    VARCHAR(100) NOT NULL,
    age        INTEGER      NOT NULL CHECK (age >= 0 AND age <= 120),
    active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- -------------------------------------------------------------
-- Índices
-- -------------------------------------------------------------
-- Por que criar índices aqui?
-- Sem índice, o Postgres faz "sequential scan" — lê a tabela
-- inteira para encontrar os registros. Com 10k linhas isso é
-- aceitável, mas o ponto do benchmark é simular I/O real.
-- O índice faz o Postgres usar "index scan", muito mais rápido,
-- e revela diferenças reais entre os modelos de concorrência.

-- Buscas por nome (LIKE 'termo%') no endpoint /users/search
CREATE INDEX IF NOT EXISTS idx_users_name    ON users (name);

-- Filtro por cidade
CREATE INDEX IF NOT EXISTS idx_users_city    ON users (city);

-- Filtro por status ativo/inativo
CREATE INDEX IF NOT EXISTS idx_users_active  ON users (active);

-- Ordenação padrão na listagem
CREATE INDEX IF NOT EXISTS idx_users_created ON users (created_at DESC);