options(repos = c(CRAN = "https://cloud.r-project.org"))

library(mrgsolve)

mod <- mread("pk3cmt", modlib())

mod
see(mod)
param(mod)
init(mod)

mod <- mod %>% param(CL = 0.8, VC = 7, Q = 1.26, VP = 150, Q2 = 0.3, VP2 = 30, KA1 = 20, KA2 = 10, VMAX = 800, KM = 1000)

# CL : Clearance (volume/time) VC : Central volume (volume)
# Q : First inter-compartmental clearance (volume/time)
# VP : First peripheral volume (volume)
# Q2 : Second inter-compartmental clearance (volume/time)
# VP2 : Second peripheral volume (volume)
# KA1 : Absorption rate constant 1 (1/time)
# KA2 : Absorption rate constant 2 (1/time)
# VMAX : Maximum velocity (mass/time)
# KM : Michaelis Constant (mass/volume)

sim_data <- mod %>%
    ev(amt = 500, cmt = 2) %>% # dose into compartment 2
    mrgsim(end = 48, delta = 0.1) %>%
    plot()


head(sim_data)

sim_df <- as.data.frame(sim_data)

# Save to CSV
write.csv(sim_df, "FINAL_mrgsolve_simulation.csv", row.names = FALSE)
