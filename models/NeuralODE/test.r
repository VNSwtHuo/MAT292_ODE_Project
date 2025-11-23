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
library(ggplot2)

code <- "
$PARAM
CL = 5,
V1 = 20,
Q2 = 3,
V2 = 30,
Q3 = 2,
V3 = 50

$CMT CENT PERIPH1 PERIPH2

$INIT CENT=0 PERIPH1=0 PERIPH2=0

$DES
double C1 = CENT / V1;
double C2 = PERIPH1 / V2;
double C3 = PERIPH2 / V3;

dxdt_CENT    = -(CL/V1)*C1 - (Q2/V1)*C1 + (Q2/V2)*C2
               - (Q3/V1)*C1 + (Q3/V3)*C3;

dxdt_PERIPH1 =  (Q2/V1)*C1 - (Q2/V2)*C2;

dxdt_PERIPH2 =  (Q3/V1)*C1 - (Q3/V3)*C3;

$TABLE
double CP = CENT / V1;
capture CP C2 C3;
"

mod <- mcode("pk3", code)

evnt <- ev(amt = 100, cmt = 1) # dose into CENT

out <- mod %>%
    ev(evnt) %>%
    mrgsim(end = 24, delta = 0.1)
out_df <- as.data.frame(out)

write.csv(out_df, "three_compartment_simulation.csv", row.names = FALSE)
print("Saved CSV!")

ggplot(out_df, aes(time, CP)) +
    geom_line(color = "blue")
