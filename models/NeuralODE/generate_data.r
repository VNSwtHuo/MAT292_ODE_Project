options(repos = c(CRAN = "https://cloud.r-project.org"))

library(mrgsolve)
# library(dplyr)

mod <- mread("pk3cmt", modlib())

mod
see(mod)
param(mod)
init(mod)


'''
sim_data <- mod %>% param(CL = 0.6, VC = 16.823472, Q = 0.320071, VP = 2.999821, Q2 = 0.320071, VP2 = 40, KA1 = 0.01902526, KA2 = 0.106696, VMAX = 329.539, KM = 17334.977)
> sim_data <- mod %>%
+     ev(amt = 100, cmt = 2) %>% # dose into compartment 2
+     mrgsim(end = 72, delta = 0.2)
> sim_df <- as.data.frame(sim_data)
> write.csv(sim_df, "mrgsolve_simulation_final.csv", row.names = FALSE)
'''

# mod <- mod %>% param(CL = 0.85, VC = 16.823472, Q = 0.320071, VP = 2.999821, Q2 = 0.320071, VP2 = 20, KA1 = 0.04951, KA2 = 0.04332, VMAX = 329.539, KM = 17334.977)

# mod <- mod %>% param(CL = 1, VC = 16.823472, Q = 0.320071, VP = 2.999821, Q2 = 0.320071, VP2 = 33.9, KA1 = 0.181, KA2 = 0.116, VMAX = 329.539, KM = 17334.977)

# mod <- mod %>% param(CL = 1, VC = 6.3, Q = 0.320071, VP = 227.7, Q2 = 0.320071, VP2 = 33.9, KA1 = 0.181, KA2 = 0.116, VMAX = 329.539, KM = 17334.977)


mod <- mod %>% param(CL = 0.6, VC = 16.823472, Q = 0.320071, VP = 2.999821, Q2 = 0.320071, VP2 = 40, KA1 = 0.01902526, KA2 = 0.106696, VMAX = 329.539, KM = 17334.977)



mod <- mod %>% param(CL = 0.8, VC = 7, Q = 4.5, VP = 30, Q2 = 6.0, VP2 = 150, KA1 = 1.2, KA2 = 0.3, VMAX = 150, KM = 15)

mod <- mod %>% param(CL = 0.8, VC = 7, Q = 1.26, VP = 150, Q2 = 0.3, VP2 = 30, KA1 = 20, KA2 = 10, VMAX = 800, KM = 1000)

mod <- mod %>% param(CL = 0.8, VC = 7, Q = 1.26, VP = 150, Q2 = 0.3, VP2 = 30, KA1 = 20, KA2 = 10, VMAX = 800, KM = 1000)

# CL
# VC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.
# Q: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.
# VP: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.
# Q2: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.
# VP2: arbitrary
# KA1: calculated Q/V1
# KA2: calcaulated Q/V2
# VMAX: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.
# KM: https://pmc.ncbi.nlm.nih.gov/articles/PMC9671373/#:~:text=Abstract,by%20fitting%20to%20literature%20data.

sim_data <- mod %>%
    ev(amt = 500, cmt = 2) %>% # dose into compartment 2
    mrgsim(end = 24, delta = 0.01) %>%
    plot()


# 0.01902526
# 0.1066
head(sim_data)

sim_df <- as.data.frame(sim_data)
# Save to CSV
write.csv(sim_data, "mrgsolve_simulation.csv", row.names = FALSE)

write.csv(sim_df, "FINAL_mrgsolve_simulation.csv", row.names = FALSE)
