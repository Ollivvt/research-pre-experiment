import pandas as pd

# Load the Excel and CSV files
file1_path = 'X:/Data/YuTing/chexpert-demodata/CHEXPERT DEMO.xlsx'  # Path for Excel file
file2_path = 'X:/Data/YuTing/CheXpert/val_labels_590.csv'  # Path for CSV file

# Read the Excel and CSV files
file1_df = pd.read_excel(file1_path)  # Read the Excel file
file2_df = pd.read_csv(file2_path)    # Read the CSV file

# Extract the full patient ID (including "patient" prefix) from the path in file2
file2_df['PATIENT'] = file2_df['Path'].str.extract(r'(patient\d+)')

# Merge file1's 'PATIENT' and 'PRIMARY_RACE' into file2
merged_df = pd.merge(file2_df, file1_df[['PATIENT', 'PRIMARY_RACE']], on='PATIENT', how='left')

# Save the merged dataframe to a new CSV file
output_file_path = 'merged_val_labels.csv'  # Define your output file path
merged_df.to_csv(output_file_path, index=False)

print(f"File saved as {output_file_path}")

