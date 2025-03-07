import pandas as pd

# Load the CSV files into DataFrames
file1_path = 'U:/GitHub/AI-ethnicity-med-image/data/NLST_CT_withPID.csv' 
file2_path = 'E:/Data/NLST/Participant Information.csv' 

# Read the CSV files
df1 = pd.read_csv(file1_path, dtype=str) 
df2 = pd.read_csv(file2_path, dtype=str)

# Match the patient ID and find their race
df1 = df1.merge(df2[['pid', 'ethnic']], left_on='Subject ID', right_on='pid', how='left')

# Optionally rename the 'race' column in df1 for clarity
df1.rename(columns={'ethnic': 'Ethnicity'}, inplace=True)

# Drop the 'pid' column if not needed
df1.drop(columns=['pid'], inplace=True)

# Remove completely empty columns
df1 = df1.dropna(axis=1, how='all')

# Save the combined DataFrame to a new CSV file
output_path = 'U:/GitHub/AI-ethnicity-med-image/data/NLST_CT_withPID_1.csv'
df1.to_csv(output_path, index=False)

print("New CSV file with combined race information has been created.")
