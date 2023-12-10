#install.packages("mirt")
library(mirt)

#install.packages("tidyverse")
library(tidyverse)

# install.packages("devtools")
# devtools::install_github("masurp/ggmirt")
library(ggmirt)

#Lê os dados do arquivo
dados <- read.delim("F:/Niedson Emanoel/Desktop/dados.txt", header = FALSE)
View(dados)

#Dados simulados
# dados <- sim_irt(1600, 15)

#Ajusta o modelo TRI 3PL
mod3 <- mirt(dados, 1, itemtype = '3PL')

#Extrai os coeficientes e salva em um data frame
coeficientes <- coef(mod3, simplify=TRUE, IRTpars=TRUE)
round(coeficientes$items, 3)

#Especifica o caminho do arquivo CSV de saída
caminho_saida <- "resultados_coef.csv"

#Escreve os coeficientes no arquivo CSV
write.csv(coeficientes, file = caminho_saida, row.names = FALSE)


#Plots e outras análises...

plot(mod3)

#Infit: Pessoas de alto theta errando questões fáceis
#Outfit: pessoas de baixo theta acertando questões difíceis
itemfitPlot(mod3)

#FitPlots
personfitPlot(mod3)

#FitPlots
itempersonMap(mod3)

tracePlot(mod3)

tracePlot(mod3, facet = F, legend = T) + scale_color_brewer(palette = "Set1")

tracePlot(mod3,items = c(1:3), facet = F, legend = T) + scale_color_brewer(palette = "Set2")

itemInfoPlot(mod3, facet = T)

testInfoPlot(mod3, adj_factor = 2)


# Calcula as pontuações latentes (notas) dos participantes
notas <- (fscores(mod3, method = 'EAP')*100)+500

#Correlacao das Notas
sumscore <- rowSums(data)
cor.test(notas, sumscore)

# Adiciona as pontuações latentes ao conjunto de dados original
dados_com_notas <- cbind(dados, notas)

# Visualiza o conjunto de dados com as pontuações latentes
View(dados_com_notas)

# Salva o conjunto de dados com as pontuações latentes em um arquivo CSV
write.csv(dados_com_notas, file = "dados_com_notas.csv", row.names = FALSE)

