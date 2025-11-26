select 
    cadclientes.Nome, 
    cadclientes.Email, 
    cadclientes.Telefone, 
    cadclientes.Cpf,
    cadclientes.Cep,
    cadplanos.Nome as PlanoAtivo, 
    cadsituacaoassinaturas.Nome as SituacaoNome,
    cadcategorias.Descricao as CategoriaNome,
    movcadclientesassinaturas.DataHora as DataAssinaturaPlano,
    cadclientes.DataCadastro as DataCadastroCliente
from movcadclientesassinaturas 
inner join cadclientes on movcadclientesassinaturas.Fk_CadClientes  = cadclientes.Id
inner join cadplanos on movcadclientesassinaturas.Fk_CadPlanos = cadplanos.Id
inner join cadsituacaoassinaturas on movcadclientesassinaturas.Fk_CadSituacaoAssinaturas = cadsituacaoassinaturas.Id
inner join cadcategorias on cadplanos.Fk_CadCategorias = cadcategorias.Id
where cadclientes.Nome not like "%teste%"
order by cadclientes.DataCadastro;