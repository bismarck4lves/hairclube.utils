CREATE VIEW vw_status_assinatura_plano AS
SELECT
    cli.email AS email,
    cli.telefone,
    cli.cpf,
    pgto.nome AS CodicaoDePagamento,
    plano.nome AS Plano,
    status.Nome AS Status,
    status.Descricao AS Descricao_status,
    main.valor AS Valor,
    main.DataHora as dataCadastro,
    main.DataCancelamento
FROM MovCadClientesAssinaturas AS main
JOIN cadclientes AS cli 
    ON cli.id = main.fk_cadClientes
JOIN cadcondpagto AS pgto 
    ON pgto.id = main.fk_cadCondPagto
JOIN cadplanos AS plano 
    ON plano.id = main.fk_cadPlanos
JOIN cadsituacaoassinaturas AS status 
    ON status.id = main.fk_cadSituacaoAssinaturas;