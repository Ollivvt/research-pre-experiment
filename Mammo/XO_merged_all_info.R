library(readxl)
library(dplyr)
library(stringr)
library(lubridate)
library(openxlsx)

# Input files
file1 <- "U:/GitHub/research-pre-experiment/Mammo/outputs/VX vs Outcomes/XRay505_Unmatched_File.csv"
file2 <- "U:/GitHub/research-pre-experiment/Mammo/outputs/mammoPatient/ethnicity_patient_records(splitFrom2019).csv"

# Load the files
df1 <- read.csv(file1)
df2 <- read.csv(file2)

# Clean and prepare df1
df1 <- df1 %>%
  mutate(
    MatchingLastName = str_split_fixed(PatientName, "\\^", 2)[, 1],  # Extract before first '^'
    MatchingLastName = toupper(MatchingLastName),  # Convert to uppercase for matching
    PatientDOB = as.Date(as.character(PatientDOB), format = "%Y%m%d"),  # Convert YYYYMMDD to date
    # StudyDate = as.Date(as.character(StudyDate), format = "%Y%m%d")  # Convert YYYYMMDD to date
  )

# Clean and prepare df2
df2 <- df2 %>%
  mutate(
    last_name = toupper(last_name),  # Convert to uppercase for matching
    date_of_birth = case_when(
      str_detect(date_of_birth, "^[0-9]{8}$") ~ as.Date(date_of_birth, format = "%Y%m%d"),      # YYYYMMDD
      str_detect(date_of_birth, "-") ~ as.Date(date_of_birth, format = "%d-%m-%Y"),  # If format is DD-MM-YYYY
      TRUE ~ NA_Date_  # Handle unexpected formats
    )
    #screen_date = case_when(
    #  str_detect(screen_date, "-") ~ as.Date(screen_date, format = "%d-%m-%Y"),  # If format is DD-MM-YYYY
    #  TRUE ~ NA_Date_  # Handle unexpected formats
    #)
  )


# Perform the merge based on PatientName, PatientDOB, and StudyDate
merged_df <- df1 %>%
  inner_join(df2, by = c("MatchingLastName" = "last_name", 
                         "PatientDOB" = "date_of_birth"), 
             relationship = "many-to-many")

# Save the merged data to an Excel file
write.csv(merged_df, "XRay505_XWalk_Outcome_matching.csv", row.names = FALSE)

cat("Merged results saved to CSV file: XRay505_XWalk_Outcome_matching.csv\n")
