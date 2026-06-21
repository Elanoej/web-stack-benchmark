-- Extensão para gerar UUIDs nativamente no Postgres
-- Em vez de deixar a aplicação gerar o ID, o banco faz isso.
-- Vantagem: menos round-trips, IDs garantidamente únicos.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

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

CREATE INDEX IF NOT EXISTS idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_city_trgm ON users USING GIN (city gin_trgm_ops);

CREATE INDEX IF NOT EXISTS indx_users_active_created ON users (active, created_at DESC);
