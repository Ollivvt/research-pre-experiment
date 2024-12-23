# Load necessary libraries
library(readxl)
library(dplyr)

# Path to the Excel file
excel_file <- "U:/GitHub/research-pre-experiment/Mammo/outputs/VX vs Outcomes/All_XWalk_Outcome_matching.xlsx"

# Get sheet names from the Excel file
sheet_names <- excel_sheets(excel_file)

# Read all sheets and combine them into one dataframe
combined_data <- lapply(sheet_names, function(sheet) {
  # Read each sheet
  data <- read_excel(excel_file, sheet = sheet)
  
  # Convert OriginalID column to character if it exists
  if ("OriginalID" %in% colnames(data)) {
    data$OriginalID <- as.character(data$OriginalID)
  }
  
  # Filter out rows where 'FilePath' is NA or empty
  data <- data %>% filter(!is.na(FilePath) & FilePath != "")
  
  return(data)
}) %>%
  bind_rows()  # Combine all sheets

# Write the combined data to a CSV file
write.csv(combined_data, "All_XWalk_Outcome_cleaned.csv", row.names = FALSE)
