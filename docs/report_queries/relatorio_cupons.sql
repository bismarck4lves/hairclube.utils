select 
cadclientes.Nome as NomeCliente,
cupomdesconto.Cupom, 
pagamentos.Titulo, 
if(cupomdesconto.DescontoPorcentagem = 1, 
  concat(round(cupomdesconto.ValorDesconto),"%"), 
  concat("R$", cupomdesconto.ValorDesconto)
) as Desconto,
pagamentos.Valor as ValorFinal,
if(cupomdesconto.DescontoPorcentagem = 1,
     round(pagamentos.Valor / (1 - (cupomdesconto.ValorDesconto / pagamentos.Valor))),
     pagamentos.Valor + cupomdesconto.ValorDesconto
     ) as ValorInicial,
pagamentos.Data
from pagamentos
inner join cupomdesconto on pagamentos.Cupom = cupomdesconto.Cupom
inner join cadclientes on pagamentos.IdCliente = cadclientes.Id
where 
pagamentos.Cupom <> ''
and pagamentos.Data > '2025-02-24';