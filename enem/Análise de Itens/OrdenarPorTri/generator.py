from gerador import gerador as Gerador
from humanas import gerador_de_lista as Humanas
from natureza import gerador_de_lista as Natureza
from linguagens import gerador_de_lista as Linguagens
from matematica import gerador_de_lista as Matematica

dfItens = Gerador.Make()

Humanas.questionBalance(nome, nota_hm, dfItens)
Matematica.questionBalance(nome, nota_MT, dfItens)
Linguagens.questionBalance(nome, nota_LC, dfItens)
Natureza.questionBalance(nome, nota_CN, dfItens)