SELECT 
    cli.email AS email,
    cli.telefone,
    cli.cpf,
    pgto.nome AS CodicaoDePagamento,
    plano.nome AS Plano,
    status.Nome AS Status,
    status.Descricao AS Descricao_status,
    assinaturas.valor AS Valor,
    assinaturas.DataHora as dataCadastro,
    assinaturas.DataCancelamento,
    CASE
        WHEN job.cancelado = 0 THEN 'JOB NAO EXECUTADO'
        WHEN job.cancelado = 1 THEN 'JOB EXECUTADO'
    END AS Situacao,
    job.data_cancelamento AS Cancelamento_agendado_para

FROM cancelamento_plano_jobs job
inner JOIN MovCadClientesAssinaturas assinaturas on assinaturas.id = job.fk_movCadClientesAssinaturas
inner JOIN cadclientes cli  ON cli.id = assinaturas.fk_cadClientes
inner JOIN cadcondpagto  pgto ON pgto.id = assinaturas.fk_cadCondPagto
inner JOIN cadplanos  plano ON plano.id = assinaturas.fk_cadPlanos
inner JOIN cadsituacaoassinaturas status ON status.id = assinaturas.fk_cadSituacaoAssinaturas