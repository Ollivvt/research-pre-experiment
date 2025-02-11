library(readxl)
library(dplyr)
library(writexl)

# Load the first Excel file
file1 <- read_excel("D:/Data/YuTing/Project/BDen/XWalk/XWDataset1_9July2021.xlsx")

# Load the second Excel file from the sheet "ByCase"
file2 <- read_excel("D:/Data/YuTing/Project/BDen/Volpara/Dataset1_Screening_ByCase.xlsx", sheet = "ByCase")

# Display column names to check actual structure
print(names(file1))
print(names(file2))

# Convert column names to lowercase for consistency
colnames(file1) <- tolower(colnames(file1))
colnames(file2) <- tolower(colnames(file2))

# Ensure required columns exist
if (!"bdprojectid" %in% names(file1) | !"studydate" %in% names(file1)) {
  stop("Error: 'bdprojectid' or 'studydate' column not found in file1")
}
if (!"patientid" %in% names(file2) | !"studydate" %in% names(file2)) {
  stop("Error: 'patientid' or 'studydate' column not found in file2")
}

# Convert StudyDate to character to match formats
file1$studydate <- as.character(file1$studydate)
file2$studydate <- as.character(file2$studydate)

# Remove duplicate BDProjectID and studydate in file1
file1_unique <- file1 %>% distinct(bdprojectid, studydate, .keep_all = TRUE)

# Perform matching
matched_data <- file1_unique %>%
  inner_join(file2, by = c("bdprojectid" = "patientid", "studydate" = "studydate")) %>%
  select(bdprojectid, studydate)

# Save the result to an Excel file
write_xlsx(matched_data, "VolXW_matched.xlsx")

print("Matching complete. Output saved as 'VolXW_matched.xlsx'")

