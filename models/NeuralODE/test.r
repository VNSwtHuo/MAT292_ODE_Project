# # ---------------------------------------------------------
# # convert_rdata_to_csv.R
# #
# # Usage:
# #   1. Set input_file to the path of your .rdx / .rda / .RData file
# #   2. Set output_dir to where you want the CSV files saved
# #   3. Run: Rscript convert_rdata_to_csv.R
# # ---------------------------------------------------------

# # ---- USER SETTINGS ----
# input_file <- "/Users/vanessahuo/Downloads/caffsim/R/caffsim.rdx"   # <-- change this
# output_dir <- "output_csv"              # <-- change this

# # -----------------------
# # Create output directory if needed
# if (!dir.exists(output_dir)) {
#     dir.create(output_dir, recursive = TRUE)
# }

# # -----------------------
# # Function to load any R data file
# load_any <- function(file) {
#     e <- new.env()
#     load(file, envir = e)
#     return(as.list(e))
# }

# # -----------------------
# # Load the RDX/RData/RDA file
# cat("Loading file:", input_file, "\n")
# objs <- load_any(input_file)

# cat("Objects found:\n")
# print(names(objs))

# # -----------------------
# # Save each object as CSV
# for (name in names(objs)) {
#     obj <- objs[[name]]

#     if (is.data.frame(obj)) {
#         csv_path <- file.path(output_dir, paste0(name, ".csv"))
#         write.csv(obj, csv_path, row.names = FALSE)
#         cat("Saved:", csv_path, "\n")
#     } else {
#         cat("Skipping", name, "- not a data.frame.\n")
#     }
# }

# cat("Done.\n")


options(repos = c(CRAN = "https://cloud.r-project.org"))

library(mrgsolve)
library(dplyr)

mod <- mread("pk2", modlib())

mod %>%
    ev(amt = 100, cmt = 2) %>% # bolus dosing every 12 hours for 10 doses
    mrgsim(end = 48, delta = 0.5) %>% # simulate for 48 hours, output every 0.5 hours
    plot()
# write.csv("neural_ode_simulation.csv", row.names = FALSE)
