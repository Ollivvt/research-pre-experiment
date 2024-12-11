import pandas as pd

# Define the mapping table
ethnicity_mapping = {
    "AP": "Aboriginal People",
    "BL": "Black",
    "BR": "British Isles",
    "EA": "Asian - East and Southeast",
    "EE": "Eastern European",
    "FR": "French",
    "NE": "Northern European",
    "OT": "Other",
    "R": "Refused To Answer",
    "SA": "Asian - South",
    "SE": "South European",
    "U": "Unknown",
    "WE": "Western European"
}

# Load the CSV file
# csv_file = r'U:\GitHub\research-pre-experiment\Mammo\outputs\mammoPatient\ethnicity_patient_records.csv'
# df = pd.read_csv(csv_file)

# Load the Excel file with all sheets
excel_file = r'U:\GitHub\research-pre-experiment\Mammo\outputs\VX vs Outcomes\All_XWalk_Outcome_matching.xlsx'
sheets = pd.read_excel(excel_file, sheet_name=None)

# Combine all sheets into one DataFrame
combined_df = pd.concat(sheets.values(), ignore_index=True)

# Remove duplicate patients based on a unique identifier (e.g., 'patient_id')
unique_patients_df = combined_df.drop_duplicates(subset=['patient_id'])

# Count the total number of unique patients
unique_patient_count = unique_patients_df['patient_id'].nunique()
print(f"Total number of unique patients: {unique_patient_count}")

# Count occurrences of each code
ethnicity_counts = unique_patients_df['ethnicity'].value_counts()

# Map codes to ethnicity names
ethnicity_counts_named = ethnicity_counts.rename(index=ethnicity_mapping)

# Calculate proportions
total_count = ethnicity_counts.sum()
ethnicity_proportions = (ethnicity_counts / total_count).rename(index=ethnicity_mapping)

# Combine counts and proportions into a DataFrame
summary_df = pd.DataFrame({
    'Count': ethnicity_counts_named,
    'Proportion': ethnicity_proportions
})

# Display the result
summary_df.reset_index(inplace=True)
summary_df.columns = ['Ethnicity', 'Count', 'Proportion']

# Save the result to a CSV file
summary_df.to_csv('ethnicity_summary.csv', index=False)

# Print the result
print(summary_df)
