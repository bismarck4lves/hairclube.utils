select
	(case
		when estabelecimento.Ativo = 1 then 'Sim'
		when estabelecimento.Ativo = 0 then 'Não'
	end) as Ativo,
	estabelecimento.NomeFantasia,
	estabelecimento.RazaoSocial,
	estabelecimento.Cnpj,
	estabelecimento.Telefone,
	estabelecimento.Email,
	estabelecimento.Instagram,
	cidade.NomeCidade as Cidade,
	estado.Nome as Estado,
	(case
		when (estabelecimento.Complemento = '' or estabelecimento.Complemento is null) then
			concat(estabelecimento.Logradouro, ' Nº ', estabelecimento.Numero)
		else
			concat(estabelecimento.Logradouro, ' Nº ', estabelecimento.Numero, ' ', estabelecimento.Complemento)
	end) as Endereco,
	estabelecimento.Cep
from cadestabelecimento estabelecimento
join cidadesibge cidade on (cidade.Id = estabelecimento.Fk_CidadesIBGE)
join estadosibge estado on (estado.Id = cidade.FK_EstadosIBGE);