# if (!require("datasets")) {
#     install.packages("datasets")
#     library("datasets")
# }

# write.csv(Indometh, file = "Indometh_full.csv", row.names = FALSE)


# Choose a CRAN mirror first
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install dependencies
install.packages(c("Rcpp", "magrittr", "dplyr", "tidyr", "stringr"))

# Install mrgsolve from CRAN
install.packages("mrgsolve")

library(mrgsolve)

# Load pre-built model
mod <- modlib("1005")

# Create dosing events
e <- ev(amt = 1000, ii = 24, addl = 3) %>% ev_rep(1:10)

# Run simulation
set.seed(1234)
out <- mod %>%
    ev(e) %>%
    mrgsim(end = 24, delta = 0.1)

# Convert to data frame
sim_data <- as.data.frame(out)

# Save to CSV
write.csv(sim_data, "mrgsolve_simulation.csv", row.names = FALSE)

# Quick plot
plot(out, IPRED ~ time, col = "blue", lwd = 2)
