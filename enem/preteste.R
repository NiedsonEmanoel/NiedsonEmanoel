library(mirt)

#Lê os dados do arquivo
dados <- read.delim("F:/Niedson Emanoel/Desktop/Past2a1.txt", header=FALSE)
View(dados)

#Ajusta o modelo TRI 3PL
mod3 <- mirt(arquivo_tabulado, 1, itemtype = '3PL')

#Extrai os coeficientes e salva em um data frame
coeficientes <- coef(mod3, simplify=TRUE, IRTpars=TRUE)

#Especifica o caminho do arquivo CSV de saída
caminho_saida <- "F:/Niedson Emanoel/Desktop/resultados_coef.csv"

#Escreve os coeficientes no arquivo CSV
write.csv(coeficientes, file = caminho_saida, row.names = FALSE)

#Visualiza os coeficientes no console
print(coeficientes)

#Plots e outras análises...
plot(mod3)
plot(mod3, type='trace')
plot(mod3, type='infotrace')
