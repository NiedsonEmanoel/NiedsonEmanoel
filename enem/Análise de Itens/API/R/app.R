library(mirt)
library(plumber)

#* @apiTitle Correção TRI pela MIRT

#' Devolve a nota tri
#' @param a discriminacação
#' @param b dificuldade
#' @param c guess
#' @param re respostas 
#' @get /tri
function(a,b,c,re){
  substringsA <- strsplit(gsub("\\s", "", a), ',')[[1]]
  a <- as.numeric(substringsA)
  
  substringsB <- strsplit(gsub("\\s", "", b), ',')[[1]]
  b <- as.numeric(substringsB)
  
  substringsC <- strsplit(gsub("\\s", "", c), ',')[[1]]
  c <- as.numeric(substringsC)
  
  substringsRE <- strsplit(gsub("\\s", "", re), ',')[[1]]
  re <- as.numeric(substringsRE)

  d <- -a*b

  set.seed(123)  # Definir semente para reproduzibilidade
  num_individuals <- 20  # Número de indivíduos
  num_items <- length(b)
  
  # Adicionar prefixo "item_" aos nomes das colunas para garantir a exclusividade
  nomes_colunas <- paste("item_", seq_len(num_items), sep = "")
  dados <- matrix(sample(0:1, num_items * num_individuals, replace = TRUE), ncol = num_items, dimnames = list(NULL, nomes_colunas))
  
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
  
  re_Zero <- rep(0, length(b))
  re_Um <- rep(1, length(b))
  
  fscores_result <- fscores(mod3, response.pattern = re, method = 'EAP') * 100 + 500
  fscores_min <- fscores(mod3, response.pattern = re_Zero, method = 'EAP') * 100 + 500
  fscores_max <- fscores(mod3, response.pattern = re_Um, method = 'EAP') * 100 + 500
  
  # Extrair apenas os valores de F1
  tri <- fscores_result[, "F1"]
  tri_max <- fscores_max[, "F1"]
  tri_min <- fscores_min[, "F1"]
  
  print(tri)
  
  
  list(
    nota = tri,
    nota_max = tri_max,
    nota_min = tri_min
  )
}