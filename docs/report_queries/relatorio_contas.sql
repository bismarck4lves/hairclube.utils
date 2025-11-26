select
    c2.Cnpj,
    c2.NomeFantasia,
    c.CodBanco,
    c.Agencia,
    c.Conta,
    c.ChavePix
from cadestabelecimentocontabancaria c
join cadestabelecimento c2 on (c2.Id = c.Fk_CadEstabelecimento)
where c.Agencia != '0000';