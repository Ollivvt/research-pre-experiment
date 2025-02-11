library(readxl)
library(dplyr)
library(writexl)

# Load the first matched result file
file1 <- read_excel("U:/GitHub/research-pre-experiment/Mammo/BDen/outputs/ViewVol_matched.xlsx")

# Load the second matched result file
file2 <- read_excel("U:/GitHub/research-pre-experiment/Mammo/BDen/outputs/VolXW_matched.xlsx")

# Display column names to check actual structure
print(names(file1))
print(names(file2))

# Convert column names to lowercase for consistency
colnames(file1) <- tolower(colnames(file1))
colnames(file2) <- tolower(colnames(file2))

# Ensure required columns exist
if (!"patient_id" %in% names(file1) | !"studydate" %in% names(file1)) {
  stop("Error: 'patient_id' or 'studydate' column not found in file1")
}
if (!"bdprojectid" %in% names(file2) | !"studydate" %in% names(file2)) {
  stop("Error: 'bdprojectid' or 'studydate' column not found in file2")
}

# Convert StudyDate to character to match formats
file1$studydate <- as.character(file1$studydate)
file2$studydate <- as.character(file2$studydate)

# Remove duplicate patient_id and studydate in file1
file1_unique <- file1 %>% distinct(patient_id, studydate, .keep_all = TRUE)

# Remove duplicate bdprojectid and studydate in file2
file2_unique <- file2 %>% distinct(bdprojectid, studydate, .keep_all = TRUE)

# Perform matching and select only required columns
final_matched_data <- file1_unique %>%
  inner_join(file2_unique, by = c("patient_id" = "bdprojectid", "studydate" = "studydate")) %>%
  select(patient_id, studydate, filepath, manufacturer, institutionname)

# Save the result to an Excel file
write_xlsx(final_matched_data, "D1_matched_v1.xlsx")

print("Final matching complete. Output saved as 'D1_matched_v1.xlsx'")
