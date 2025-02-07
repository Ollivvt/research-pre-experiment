# Load necessary libraries
library(dplyr)
library(readxl)

# Read the first CSV file
file1 <- read.csv("U:/GitHub/research-pre-experiment/Mammo/All_XWalk_Outcome_1.csv", stringsAsFactors = FALSE)

# Read the second Excel file
file2_sheets <- excel_sheets("D:/Data/YuTing/Project/Tabular/ViewCatalog/XRay505_ViewCount_2023-11-03.xlsx")
file2 <- bind_rows(lapply(file2_sheets, function(sheet) {
  read_excel("D:/Data/YuTing/Project/Tabular/ViewCatalog/XRay505_ViewCount_2023-11-03.xlsx", sheet = sheet)
}))

# Ensure file2 has unique `patient_id` and `FilePath`
file2_unique <- file2 %>%
  group_by(patient_id, FilePath) %>%
  summarise(
    Manufacturer_new = paste(unique(Manufacturer), collapse = "; "),
    InstitutionName_new = paste(unique(InstitutionName), collapse = "; "),
    .groups = "drop"
  )

# Merge the data without overwriting existing values
merged_data <- file1 %>%
  left_join(file2_unique, by = c("patient_id", "FilePath")) %>%
  mutate(
    Manufacturer = ifelse(is.na(Manufacturer), Manufacturer_new, 
                          ifelse(is.na(Manufacturer_new), Manufacturer, 
                                 paste(Manufacturer, Manufacturer_new, sep = "; "))),
    InstitutionName = ifelse(is.na(InstitutionName), InstitutionName_new, 
                             ifelse(is.na(InstitutionName_new), InstitutionName, 
                                    paste(InstitutionName, InstitutionName_new, sep = "; ")))
  ) %>%
  select(-Manufacturer_new, -InstitutionName_new)

# Save the merged data back to CSV
write.csv(merged_data, "U:/GitHub/research-pre-experiment/Mammo/All_XWalk_Outcome.csv", row.names = FALSE)