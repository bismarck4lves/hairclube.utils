

CREATE VIEW vw_agendamentos_cliente AS
SELECT 
    s.Nome AS servico,
    e.NomeFantasia AS salao,
    p.nome AS plano,
    c.id as client_id,
    c.nome AS client_nome,
    c.cpf AS client_cpf,
    c.email AS client_email,
    c.telefone AS client_telefone,
    main.DataHora AS data_do_agendamento,
    main.DataAgendamento AS agendado_para,
    main.Situacao AS situacao_codigo,
    main.DataReagendamento AS data_do_cancelamento,
    main.OrigemCancelamento,
    CASE
        WHEN main.Situacao = 1 THEN 'Confirmado'
        WHEN main.Situacao = 2 THEN 'Realizado'
        WHEN main.Situacao = 3 THEN 'Pendente'
        WHEN main.Situacao = 4 THEN 'Cancelado'
    END AS Situacao

FROM movcadclientesconsumo main 
JOIN cadestabelecimentoservicosusuarios esu ON esu.id = main.Fk_CadEstabelecimentoServicosUsuarios
JOIN cadestabelecimentoservicos es ON es.id = esu.Fk_CadEstabelecimentoServicos
JOIN cadservicos s ON s.id = es.Fk_CadServicos
JOIN cadestabelecimento e ON e.id = es.Fk_CadEstabelecimento
JOIN cadclientes c ON c.id = main.fk_cadClientes
JOIN cadplanos p ON p.id = main.Fk_CadPlanos

