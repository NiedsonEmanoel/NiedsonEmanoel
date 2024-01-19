#SCRIPT PARA PARÂMETROS JÁ FITADOS!

#install.packages("mirt")
library(mirt)

#install.packages("tidyverse")
library(tidyverse)

# install.packages("devtools")
# devtools::install_github("masurp/ggmirt")
library(ggmirt)


caminho_pasta_script <- getwd()

#SEM HEADER
caminho_leitura <- file.path(caminho_pasta_script, "dados.txt")
dados <- read.delim(caminho_leitura, header = FALSE)

#CSV COM HEADER
caminho_leitura <- file.path(caminho_pasta_script, "dados.csv")
dados <- read.table(caminho_leitura, sep=',', header = TRUE)

#COM HEADER
# caminho_leitura <- file.path(caminho_pasta_script, "dados.txt")
# dados <- read.delim(caminho_leitura, header = TRUE)

#Dados simulados

# dados <- sim_irt(500, 45)

View(dados)

caminho_leitura <- file.path(caminho_pasta_script, "datatri.csv")
dataParam = read.table(caminho_leitura, sep=',', h=T)
View(dataParam)

a <- as.numeric(gsub(",", ".", dataParam[,8]))

class(a)
b <- as.numeric(gsub(",", ".", dataParam[,9]))
c <- as.numeric(gsub(",", ".", dataParam[,10]))


d <- -a*b
#COLOCANDO VALORES PADRÕES NOS ITENS
sv <- mirt(dados, 1, itemtype = '3PL', pars = 'values')

#PARAMETRO A                  #I1 #I2  #I3...
sv$value[sv$name == 'a1'] <- a

#PARAMETRO B
sv$value[sv$name == 'd'] <- d

#PARAMETRO C
sv$value[sv$name == 'g'] <- c
sv$est <- FALSE

#CRIAÇÃO DO MODELO
mod3 <- mirt(dados, 1, pars = sv)
#Extrai os coeficientes e salva em um data frame
coeficientes <- coef(mod3, simplify=TRUE, IRTpars=TRUE)
round(coeficientes$items, 3)

#Especifica o caminho do arquivo CSV de saída
caminho_saida <- file.path(caminho_pasta_script, "resultados_coef.csv")

#Escreve os coeficientes no arquivo CSV
write.csv(coeficientes, file = caminho_saida, row.names = FALSE)

#Plots e outras análises...

#Comportamento Exame
scaleCharPlot(mod3)

#Infit: Pessoas de alto theta errando questões fáceis
#Outfit: pessoas de baixo theta acertando questões difíceis
itemfitPlot(mod3)

#FitPlots
#(Distribuição da população em infit e outfit)
personfitPlot(mod3)

#FitPlots
#Comportamento do Exame em Theta
itempersonMap(mod3)

#CCI ITENS
tracePlot(mod3)

#CCI TODOS OS ITENS
tracePlot(mod3, facet = F, legend = T) + scale_color_brewer(palette = "Set1")

#CCI ITENS SELECIONADOS
tracePlot(mod3,items = c(1:5), facet = F, legend = T) + scale_color_brewer(palette = "Set2")

#INFORMAÇÃ0 CURVAS ITENS
itemInfoPlot(mod3, facet = T)

# INFORMAÇÀO DO TESTE (NOTAS MAX E MIN)
testInfoPlot(mod3, adj_factor = 2)

# Calcula as pontuações latentes (notas) dos participantes
notas <- (fscores(mod3, method = 'EAP')*100)+500
View(notas)
#F1 - PARA RESPOSTAS MÁXIMAS

fscores_result <- fscores(mod3, response.pattern = c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), method = 'EAP') * 100 + 500

# Extrair apenas os valores de F1
l <- fscores_result[, "F1"]

# Mostrar os valores de F1
print(l)

#F1 - PARA RESPOSTAS MÍNIMAS
(fscores(mod3, response.pattern = c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), method = 'EAP')*100)+500

#Correlacao das Notas
sumscore <- rowSums(dados)
cor.test(notas, sumscore)

# Adiciona as pontuações latentes ao conjunto de dados original
dados_com_notas <- cbind(dados, notas)

# Visualiza o conjunto de dados com as pontuações latentes
View(dados_com_notas)

# Salva o conjunto de dados com as pontuações latentes em um arquivo CSV
caminho_saida <- file.path(caminho_pasta_script, "dados_com_notas.csv")
write.csv(dados_com_notas, file = caminho_saida, row.names = FALSE)
