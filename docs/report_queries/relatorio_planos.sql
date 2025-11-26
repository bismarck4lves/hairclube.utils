Select
cliente.Nome as Cliente,
estab.NomeFantasia as Salao,
servico.Nome as Servico,
Cp.Nome as Plano,
category.Descricao as Categoria,
ctestab.Descricao as CategoriaSalao,
Mc.DataAgendamento as DataAgendamento,
CASE
    WHEN Mc.Situacao = 1 THEN 'Confirmado'
    WHEN Mc.Situacao = 2 THEN 'Realizado'
    WHEN Mc.Situacao = 3 THEN 'Pendente'
    WHEN Mc.Situacao = 4 THEN 'Cancelado'
END AS Situacao,
concat('R$', FORMAT(Csr.Valor, 2)) AS Valor
From MovCadClientesConsumo Mc
Join CadEstabelecimentoServicosUsuarios Cesu on (Cesu.Id = Mc.Fk_CadEstabelecimentoServicosUsuarios)
Join CadEstabelecimentoServicos Ces on (Ces.Id = Cesu.Fk_CadEstabelecimentoServicos)
left join cadservicos servico on servico.Id = Ces.Fk_CadServicos
join cadestabelecimento estab on estab.Id = Ces.Fk_CadEstabelecimento
Join CadPlanos Cp on (Cp.Id = Mc.Fk_CadPlanos)
join cadcategorias category on category.Id = Cp.Fk_CadCategorias
JOIN cadestabelecimentocategoria cec
    ON cec.Fk_CadEstabelecimento = estab.Id
    AND cec.Ativo = 1
    AND cec.Id = (
        SELECT MAX(Id)
        FROM cadestabelecimentocategoria
        WHERE Fk_CadEstabelecimento = estab.Id
        AND Ativo = 1
    )
join cadcategorias ctestab on ctestab.Id = cec.Fk_CadCategorias
Join CadServicosRepasseCategoria Csr on (Csr.Fk_CadCategorias = cec.Fk_CadCategorias) and (Csr.Fk_CadServicos = Ces.Fk_CadServicos)
join cadclientes cliente on cliente.Id = Mc.Fk_CadClientes
where cliente.Nome not like "%teste%"
order by estab.NomeFantasia, Cp.Nome, servico.Nome, Mc.DataAgendamento, Mc.Situacao;