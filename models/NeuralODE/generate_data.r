options(repos = c(CRAN = "https://cloud.r-project.org"))

library(mrgsolve)
library(dplyr)

mod <- mread("pk3cmt", modlib())

sim_data <- mod %>%
    ev(amt = 100, cmt = 2) %>% # dose into compartment 2
    mrgsim(end = 48, delta = 0.5)
plot()

head(sim_data)

# Save to CSV
write.csv(sim_data, "mrgsolve_simulation.csv", row.names = FALSE)
