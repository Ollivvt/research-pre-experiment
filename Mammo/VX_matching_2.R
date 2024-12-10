library(readxl)
library(dplyr)
library(stringr)
library(openxlsx)

# Input files
file1 <- "D:/Data/YuTing/Project/Tabular/ViewCatalog/BCWomen_ViewCount_2023-11-04.xlsx"
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

# Initialize lists for matched and mismatched results
matched_list <- list()
mismatched_list <- list()

# Count processed rows
total_processed <- 0

# Iterate over each sheet in df1
for (i in seq_along(df1_list)) {
  sheet_name <- file1_sheets[i]
  df1 <- df1_list[[i]]
  
  # Clean columns in df1
  df1 <- clean_column(df1, "patient_id")
  df1 <- studydate_as_char(df1, "StudyDate")
  df1 <- clean_accession(df1, "AccessionNumber")
  
  # Ensure columns exist or fill missing
  if (!"InstitutionName" %in% names(df1)) df1$InstitutionName <- NA
  if (!"Manufacturer" %in% names(df1)) df1$Manufacturer <- NA
  
  df1$InstitutionName[is.na(df1$InstitutionName)] <- ""
  df1$Manufacturer[is.na(df1$Manufacturer)] <- ""
  
  # Iterate through rows of df1
  for (r in seq_len(nrow(df1))) {
    row1 <- df1[r, ]
    total_processed <- total_processed + 1  # Track processed rows
    
    # Skip rows where patient_id, StudyDate, and AccessionNumber are all empty
    if ((is.na(row1$patient_id) || row1$patient_id == "") &&
        (is.na(row1$StudyDate) || row1$StudyDate == "") &&
        (is.na(row1$AccessionNumber) || row1$AccessionNumber == "")) {
      mismatched_list[[length(mismatched_list) + 1]] <- data.frame(
        Mismatch_Reason = "Empty Record",
        patient_id_file1 = row1$patient_id,
        patient_id_file2 = "",
        StudyDate_file1 = row1$StudyDate,
        StudyDate_file2 = "",
        AccessionNumber_file1 = row1$AccessionNumber,
        AccessionNumber_file2 = "",
        InstitutionName_file1 = row1$InstitutionName,
        InstitutionName_file2 = "",
        Manufacturer_file1 = row1$Manufacturer,
        Sheet = sheet_name,
        stringsAsFactors = FALSE
      )
      next
    }
    
    # Matching only by patient_id and StudyDate
    match_cond <- df2$BDProjectID == row1$patient_id & df2$StudyDate == row1$StudyDate
    match_rows <- df2[match_cond, , drop = FALSE]
    
    if (nrow(match_rows) > 0) {
      # Take the first matched row (if multiple)
      matched_list[[length(matched_list) + 1]] <- data.frame(
        patient_id = row1$patient_id,
        StudyDate = row1$StudyDate,
        AccessionNumber = row1$AccessionNumber,
        Sheet = sheet_name,
        stringsAsFactors = FALSE
      )
    } else {
      # No direct match found
      mismatched_list[[length(mismatched_list) + 1]] <- data.frame(
        Mismatch_Reason = "No Match Found",
        patient_id_file1 = row1$patient_id,
        patient_id_file2 = "",
        StudyDate_file1 = row1$StudyDate,
        StudyDate_file2 = "",
        AccessionNumber_file1 = row1$AccessionNumber,
        AccessionNumber_file2 = "",
        InstitutionName_file1 = row1$InstitutionName,
        InstitutionName_file2 = "",
        Manufacturer_file1 = row1$Manufacturer,
        Sheet = sheet_name,
        stringsAsFactors = FALSE
      )
    }
  }
}

# Combine matched and mismatched lists into data frames
matched_df <- if (length(matched_list) > 0) {
  do.call(rbind, matched_list)
} else {
  data.frame(patient_id = character(), StudyDate = character(), AccessionNumber = character(), Sheet = character(), stringsAsFactors = FALSE)
}

mismatched_df <- if (length(mismatched_list) > 0) {
  do.call(rbind, mismatched_list)
} else {
  data.frame(Mismatch_Reason = character(), patient_id_file1 = character(), patient_id_file2 = character(),
             StudyDate_file1 = character(), StudyDate_file2 = character(),
             AccessionNumber_file1 = character(), AccessionNumber_file2 = character(),
             InstitutionName_file1 = character(), InstitutionName_file2 = character(),
             Manufacturer_file1 = character(), Sheet = character(), stringsAsFactors = FALSE)
}

# Verify row count consistency
total_matched <- nrow(matched_df)
total_mismatched <- nrow(mismatched_df)
total_file1 <- sum(sapply(df1_list, nrow))

cat("Row count summary:\n")
cat("Total rows in file1:", total_file1, "\n")
cat("Total matched rows:", total_matched, "\n")
cat("Total mismatched rows:", total_mismatched, "\n")
cat("Total processed rows:", total_processed, "\n")

if (total_processed != total_file1) {
  warning("Row count mismatch: some rows may not have been processed.")
}


# Save results to Excel
write.xlsx(matched_df, "BCWomen_matched_list.xlsx", overwrite = TRUE)
write.xlsx(mismatched_df, "BCWomen_mismatched_list.xlsx", overwrite = TRUE)

cat("Results saved to Excel files.\n")
