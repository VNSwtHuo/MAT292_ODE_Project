if(!require('datasets')) {
    install.packages('datasets')
    library('datasets')
}

write.csv(Theoph, file = "Theoph_full.csv", row.names = FALSE)


