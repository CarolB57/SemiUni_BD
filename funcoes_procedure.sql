/*


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


*/

CREATE OR REPLACE FUNCTION data_certificado()
RETURNS DATE
LANGUAGE plpgsql
AS $$
DECLARE
    dia INTEGER;
BEGIN
    -- Gera número aleatório entre 15 e 30
    dia := 15 + FLOOR(random() * 16)::INT;

    -- Retorna a data correspondente em novembro de 2025
    RETURN make_date(2025, 11, dia);
END;
$$;

CREATE OR REPLACE FUNCTION gerar_numero(n INTEGER)
RETURNS BIGINT
LANGUAGE plpgsql
AS $$
DECLARE
	minimo BIGINT;
    maximo BIGINT;
BEGIN
	IF n < 1 THEN
        RAISE EXCEPTION 'Número de dígitos deve ser >= 1';
    END IF;

    minimo := 10 ^ (n - 1);
    maximo := (10 ^ n) - 1;

    RETURN minimo + FLOOR(random() * (maximo - minimo + 1))::BIGINT;
END;
$$;