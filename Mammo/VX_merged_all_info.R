library(readxl)
library(dplyr)
library(stringr)
library(openxlsx)

# Input files
file1 <- "D:/Data/YuTing/Project/Tabular/ViewCatalog/Burnaby_ViewCount_2023-11-03.xlsx"
file2 <- "D:/Data/YuTing/Project/Tabular/XWalk/XW.xlsx"

# Load all sheets from file1 into a list of data frames
file1_sheets <- excel_sheets(file1)
df1_list <- lapply(file1_sheets, function(s) read_excel(file1, sheet = s))

# Load file2
df2 <- read_excel(file2)

# Function to clean a given column
clean_column <- function(df, column) {
  df[[column]] <- tolower(str_trim(as.character(df[[column]])))
  df[[column]][df[[column]] == "nan"] <- NA
  df
}

# Function to clean AccessionNumber: treat '-' as empty
clean_accession <- function(df, column) {
  df[[column]] <- as.character(df[[column]])
  df[[column]][str_detect(df[[column]], "-")] <- NA
  df[[column]][is.na(df[[column]])] <- ""
  df
}

# Handle StudyDate as character
studydate_as_char <- function(df, date_col) {
  df[[date_col]] <- str_trim(as.character(df[[date_col]]))
  df
}

# Clean and standardize df2
df2 <- clean_column(df2, "BDProjectID")
df2 <- studydate_as_char(df2, "StudyDate")
df2 <- clean_accession(df2, "AccessionNum")

# Initialize list for merged results
merged_list <- list()

# Iterate over each sheet in df1
for (i in seq_along(df1_list)) {
  sheet_name <- file1_sheets[i]
  df1 <- df1_list[[i]]
  
  # Clean columns in df1
  df1 <- clean_column(df1, "patient_id")
  df1 <- studydate_as_char(df1, "StudyDate")
  df1 <- clean_accession(df1, "AccessionNumber")
  
  # Ensure additional columns exist in df1 or fill missing
  if (!"FilePath" %in% names(df1)) df1$FilePath <- NA
  if (!"InstitutionName" %in% names(df1)) df1$InstitutionName <- NA
  df1$InstitutionName[is.na(df1$InstitutionName)] <- ""
  
  # Iterate through rows of df1
  for (r in seq_len(nrow(df1))) {
    row1 <- df1[r, ]
    
    # Skip rows where patient_id, StudyDate, and AccessionNumber are all empty
    if ((is.na(row1$patient_id) || row1$patient_id == "") &&
        (is.na(row1$StudyDate) || row1$StudyDate == "") &&
        (is.na(row1$AccessionNumber) || row1$AccessionNumber == "")) {
      next
    }
    
    # Matching only by patient_id and StudyDate
    match_cond <- df2$BDProjectID == row1$patient_id & df2$StudyDate == row1$StudyDate
    match_rows <- df2[match_cond, , drop = FALSE]
    
    if (nrow(match_rows) > 0) {
      # Take the first matched row (if multiple)
      match_row <- match_rows[1, ]
      
      # Create a merged result row
      merged_list[[length(merged_list) + 1]] <- data.frame(
        patient_id = row1$patient_id,
        PatientName = match_row$PatientName,
        PatientDOB = match_row$PatientDOB,
        OriginalID = match_row$OriginalID,
        StudyDate = row1$StudyDate,
        AccessionNumber = row1$AccessionNumber,
        FilePath = row1$FilePath,
        SheetName = sheet_name,
        stringsAsFactors = FALSE
      )
    }
  }
}

# Combine merged results into a data frame
merged_df <- if (length(merged_list) > 0) {
  do.call(rbind, merged_list)
} else {
  data.frame(patient_id = character(), PatientName = character(), 
             PatientDOB = character(), OriginalID = character(),
             StudyDate = character(), AccessionNumber = character(),
             FilePath = character(), SheetName = character(),
             stringsAsFactors = FALSE)
}

# Save results to Excel
write.xlsx(merged_df, "Burnaby_merged_list.xlsx", overwrite = TRUE)

cat("Merged results saved to Excel file.\n")
