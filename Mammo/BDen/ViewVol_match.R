library(readxl)
library(dplyr)
library(writexl)

# Load the first Excel file from the sheet "DS1-Screening"
file1 <- read_excel("D:/Data/YuTing/Project/BDen/ViewCount/DS1_ViewCount_2023-09-14.xlsx", sheet = "DS1-Screening")

# Load the second Excel file from the sheet "ByCase"
file2 <- read_excel("D:/Data/YuTing/Project/BDen/Volpara/Dataset1_Screening_ByCase.xlsx", sheet = "ByCase")

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
if (!"patientid" %in% names(file2) | !"studydate" %in% names(file2)) {
  stop("Error: 'patientid' or 'studydate' column not found in file2")
}

# Convert StudyDate to character to match formats
file1$studydate <- as.character(file1$studydate)
file2$studydate <- as.character(file2$studydate)

# Remove duplicate patient_id and studydate in file1
file1_unique <- file1 %>% distinct(patient_id, studydate, .keep_all = TRUE)

# Perform matching and select only required columns
matched_data <- file1_unique %>%
  inner_join(file2, by = c("patient_id" = "patientid", "studydate" = "studydate")) %>%
  select(patient_id, studydate, filepath, manufacturer, institutionname)

# Save the result to an Excel file
write_xlsx(matched_data, "ViewVol_matched.xlsx")

print("Matching complete. Output saved as 'ViewVol_matched.xlsx'")