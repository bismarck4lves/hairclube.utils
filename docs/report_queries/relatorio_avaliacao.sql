select
	avaliacao.DataHora,
	cliente.Nome as Cliente,
	estabelecimento.NomeFantasia as Estabelecimento,
	avaliacao.Estabelecimento as Avaliacao,
	profissional.Nome as Profissional,
	avaliacao.Profissional as Avaliacao,
	avaliacao.Observacao
from movcadclientesconsumoavaliacao avaliacao
left join movcadclientesconsumo consumo on (consumo.Id = avaliacao.Fk_MovCadClientesConsumo)
left join cadclientes cliente on (cliente.Id = consumo.Fk_CadClientes)
left join cadestabelecimentoservicosusuarios servico on (servico.Id = consumo.Fk_CadEstabelecimentoServicosUsuarios)
left join cadestabelecimentousuarios profissional on (profissional.Id = servico.Fk_CadEstabelecimentoUsuarios)
left join cadestabelecimento estabelecimento on (estabelecimento.Id = profissional.Fk_CadEstabelecimento)
order by avaliacao.DataHora desc;