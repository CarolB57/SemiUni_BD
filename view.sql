/*


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


*/

-- View com participantes que receberam certificado em atividades realizadas no prédio UAC com presença confirmada.

CREATE VIEW CertificadosUAC AS
SELECT 
	  p.Nome AS Participante,
	  a.Tema AS Atividade,
	  l.Nome AS LocalAtividade,
	  c.Codigo AS Codigo_Certificado
	  
FROM Participante p
JOIN Inscricao i ON p.CPF = i.CPF_Participante
JOIN Atividade a ON i.Cod_Atividade = a.Codigo
JOIN Certificado c ON i.Codigo = c.Cod_Inscricao
JOIN LocalAtividade l ON a.Cod_Local = l.Codigo
WHERE 
	  i.Presenca = TRUE AND
	  l.Sigla = 'UAC';