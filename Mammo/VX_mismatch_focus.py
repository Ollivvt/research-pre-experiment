import pandas as pd

# Load the mismatched Excel file
input_file = r'U:\GitHub\research-pre-experiment\Mammo\outputs\ViewCatalog vs XWalk\Original Mismatched List\NLMMobile_mismatched_list.xlsx'
df = pd.read_excel(input_file)

# Clean Accession Numbers by removing 'MG' for comparison
df['AccessionNumber_file1_clean'] = df['AccessionNumber_file1'].str.replace('MG', '', regex=False)
df['AccessionNumber_file2_clean'] = df['AccessionNumber_file2'].str.replace('MG', '', regex=False)

# Identify matched records based on cleaned AccessionNumbers
matched_records = df[df['AccessionNumber_file1_clean'] == df['AccessionNumber_file2_clean']].copy()

# Keep unique records based on patient_id_file1 and AccessionNumber_file1
unique_matched = matched_records.drop_duplicates(subset=['patient_id_file1', 'AccessionNumber_file1'])

# Format the output for matched records
matched_output = unique_matched[['patient_id_file1', 'StudyDate_file1', 'AccessionNumber_file1', 
                                 'Sheet', 'patient_id_file2']]
matched_output.columns = ['patient_id', 'StudyDate', 
                          'AccessionNumber', 'Sheet', 
                          'patient_id (XWalk))']

# Get the patient IDs from matched output
matched_patient_ids = set(matched_output['patient_id'])

# Filter out records where patient_id_file1 is in the matched_patient_ids
remaining_mismatches = df[~df['patient_id_file1'].isin(matched_patient_ids)].copy()

# Save outputs to Excel
matched_output_file = "NLMMobile_matched_2pid.xlsx"
remaining_mismatches_file = "NLMMobile_still_mismatched_list.xlsx"

matched_output.to_excel(matched_output_file, index=False)
remaining_mismatches.to_excel(remaining_mismatches_file, index=False)

print(f"Matched records saved to {matched_output_file}")
print(f"Remaining mismatched records saved to {remaining_mismatches_file}")