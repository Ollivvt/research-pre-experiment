# Load required libraries
library(readxl)
library(dplyr)

# Define the mapping table
ethnicity_mapping <- c(
  "AP" = "Aboriginal People",
  "BL" = "Black",
  "BR" = "British Isles",
  "EA" = "Asian - East and Southeast",
  "EE" = "Eastern European",
  "FR" = "French",
  "NE" = "Northern European",
  "OT" = "Other",
  "R" = "Refused To Answer",
  "SA" = "Asian - South",
  "SE" = "South European",
  "U" = "Unknown",
  "WE" = "Western European"
)

# Load the Excel file with all sheets
excel_file <- "U:/GitHub/research-pre-experiment/Mammo/outputs/VX vs Outcomes/All_XWalk_Outcome_matching.xlsx"
sheets <- excel_sheets(excel_file)

# Combine all sheets into one data frame
combined_df <- lapply(sheets, function(sheet) {
  df <- read_excel(excel_file, sheet = sheet)
  df$OriginalID <- as.character(df$OriginalID)
  return(df)
}) %>% bind_rows()

# Remove duplicate patients based on a unique identifier (e.g., 'patient_id')
unique_patients_df <- combined_df %>% distinct(patient_id, .keep_all = TRUE)

# Count the total number of unique patients
unique_patient_count <- n_distinct(unique_patients_df$patient_id)
cat("Total number of unique patients:", unique_patient_count, "\n")

# Count occurrences of each code
ethnicity_counts <- table(unique_patients_df$ethnicity)

# Map codes to ethnicity names
ethnicity_counts_named <- setNames(as.vector(ethnicity_counts), 
                                   ethnicity_mapping[names(ethnicity_counts)])

# Calculate proportions
total_count <- sum(ethnicity_counts)
ethnicity_proportions <- ethnicity_counts / total_count

# Combine counts and proportions into a data frame
summary_df <- data.frame(
  Ethnicity = ethnicity_mapping[names(ethnicity_counts)],
  Count = as.vector(ethnicity_counts),
  Proportion = ethnicity_proportions
)

# Save the result to a CSV file
write.csv(summary_df, "ethnicity_summary_uniPatients.csv", row.names = FALSE)

# Print the result
print(summary_df)
