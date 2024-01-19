library(plumber)
r <- plumb("app.R")
# get port number from environment variable
port <- 8080
r$run(port=port, host='0.0.0.0', swagger=FALSE)