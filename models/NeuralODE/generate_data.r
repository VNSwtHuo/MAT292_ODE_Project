options(repos = c(CRAN = "https://cloud.r-project.org"))

library(mrgsolve)
# library(dplyr)

mod <- mread("pk3cmt", modlib())

mod
see(mod)
param(mod)
init(mod)

mod <- mod %>% param(CL = 50, VC = 3.5, Q = 8, VP = 10, Q2 = 2, VP2=20, KA1=0.195, KA2=6.02736, KM=5.57)


sim_data <- mod %>%
    ev(amt = 400, cmt = 2) %>% # dose into compartment 2
    mrgsim(end = 48, delta = 0.5)
plot()

head(sim_data)

# Save to CSV
write.csv(sim_data, "mrgsolve_simulation.csv", row.names = FALSE)

