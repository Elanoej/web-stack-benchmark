-- =============================================================
-- SEED — web-stack-benchmark
-- =============================================================
-- Gera 10.000 usuários com dados variados.
--
-- Por que 10.000?
-- Poucos registros (ex: 100) cabem no cache do Postgres e
-- nunca chegam no disco — o resultado seria irreal.
-- 10k é suficiente para forçar I/O real sem precisar de um
-- banco enorme. Em produção você teria milhões, mas para
-- comparar modelos de concorrência isso é suficiente.
--
-- Por que usar generate_series + random()?
-- Gera dados distribuídos de forma controlada e reproduzível.
-- Toda vez que o seed rodar vai gerar os mesmos dados
-- (porque não usamos seeds aleatórios — os nomes/cidades
-- são escolhidos por módulo, então são determinísticos).
-- =============================================================

-- Arrays de nomes e cidades para variar os dados
DO $$
DECLARE
    nomes    TEXT[] := ARRAY[
        'Ana Silva', 'Bruno Costa', 'Carla Souza', 'Diego Lima',
        'Elena Martins', 'Felipe Rocha', 'Gabriela Alves', 'Henrique Nunes',
        'Isabela Ferreira', 'João Oliveira', 'Kamila Santos', 'Lucas Pereira',
        'Mariana Castro', 'Nicolas Barbosa', 'Olivia Carvalho', 'Pedro Mendes',
        'Queila Ramos', 'Rafael Torres', 'Sofia Cardoso', 'Thiago Gomes'
    ];
    cidades  TEXT[] := ARRAY[
        'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba',
        'Porto Alegre', 'Salvador', 'Fortaleza', 'Recife',
        'Manaus', 'Belém', 'Goiânia', 'Florianópolis'
    ];
    paises   TEXT[] := ARRAY[
        'Brasil', 'Argentina', 'Chile', 'Colômbia', 'Peru'
    ];
    i        INTEGER;
    nome     TEXT;
    cidade   TEXT;
    pais     TEXT;
    idade    INTEGER;
BEGIN
    FOR i IN 1..10000 LOOP
        nome   := nomes[  (i % array_length(nomes,   1)) + 1 ];
        cidade := cidades[ (i % array_length(cidades, 1)) + 1 ];
        pais   := paises[  (i % array_length(paises,  1)) + 1 ];
        idade  := 18 + (i % 50); -- idades entre 18 e 67

        INSERT INTO users (name, email, city, country, age, active)
        VALUES (
            nome || ' ' || i,                          -- "Ana Silva 1", "Bruno Costa 2" ...
            'user' || i || '@benchmark.dev',           -- email único garantido
            cidade,
            pais,
            idade,
            (i % 10 != 0)                             -- 10% dos usuários são inativos
        );
    END LOOP;

    RAISE NOTICE 'Seed concluído: 10.000 usuários inseridos.';
END;
$$;