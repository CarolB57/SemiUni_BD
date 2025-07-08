/*

Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados

Procedure para emitir certificados para todos os participantes inscritos em pelo menos 3 atividades diferentes, 
desde que tenham foto cadastrada e não tenham recebido certificado ainda.

*/

-- CALL gerar_certificados();

CREATE OR REPLACE PROCEDURE gerar_certificados()
LANGUAGE plpgsql
AS $$
DECLARE
	participante RECORD;
	qtd_certificados INTEGER;
	inscricao RECORD;
	gerar_codigo INTEGER;
	ocupacao VARCHAR(40);
	tipo_certificado VARCHAR(30);
	v_mensagem TEXT;

	cursor_participantes CURSOR FOR
		SELECT p.CPF, p.Ocupacao FROM Participante p
		JOIN Inscricao i ON i.CPF_Participante = p.CPF
		WHERE p.Foto IS NOT NULL
		GROUP BY p.CPF
		HAVING COUNT(DISTINCT i.Cod_Atividade) >= 3;
BEGIN
	FOR participante IN cursor_participantes LOOP
		-- Verifica se o participante já tem algum certificado
		SELECT COUNT(*) INTO qtd_certificados
		FROM Certificado c
		JOIN Inscricao i ON i.Codigo = c.Cod_Inscricao
		WHERE i.CPF_Participante = participante.CPF;

		IF qtd_certificados = 0 THEN
            -- Obtém a ocupação do participante
            ocupacao := participante.Ocupacao;

            -- Gera certificados apenas para inscrições com presença confirmada
            FOR inscricao IN
                SELECT i.Codigo, i.Presenca
                FROM Inscricao AS i
                WHERE i.CPF_Participante = participante.CPF
            LOOP
                BEGIN
                    -- Verifica presença
                    IF NOT inscricao.Presenca THEN
                        RAISE NOTICE 'Inscrição %: Presença não confirmada. Nenhum certificado gerado.', inscricao.Codigo;
                        CONTINUE;
                    END IF;

                    -- Define tipo de certificado com base na ocupação
                    IF LOWER(ocupacao) IN ('aluno', 'aluna', 'visitante') THEN
                        tipo_certificado := 'Participação';
                    ELSIF LOWER(ocupacao) IN ('professor', 'professora') THEN
                        tipo_certificado := 'Ministrante Evento';
                    ELSIF LOWER(ocupacao) = 'palestrante' THEN
                        tipo_certificado := 'Ministrante Palestra';
                    ELSE
                        RAISE NOTICE 'Ocupação % não gera certificado automático.', ocupacao;
                        CONTINUE;
                    END IF;

                    -- Gera o certificado
					LOOP
						gerar_codigo := gerar_numero(7);
						EXIT WHEN NOT EXISTS (
							SELECT 1 FROM Certificado WHERE Codigo = gerar_codigo
						);
					END LOOP;
					
                    INSERT INTO Certificado (Codigo, Cod_Inscricao, Tipo, DataEmissao, Emitido)
                    VALUES(
						gerar_codigo,
						inscricao.Codigo,
						tipo_certificado,
						data_certificado(),
						TRUE
                    );

                    RAISE NOTICE 'Certificado gerado para inscrição % com tipo %', inscricao.Codigo, tipo_certificado;
                EXCEPTION WHEN OTHERS THEN
                    v_mensagem := FORMAT(
                        'Erro ao gerar certificado para inscrição %s: %s',
                        inscricao.Codigo, SQLERRM
                    );
                    RAISE WARNING '%', v_mensagem;
                END;
            END LOOP;
        ELSE
            RAISE NOTICE 'Participante % já possui certificado.', participante.CPF;
        END IF;
    END LOOP;
END;
$$;
