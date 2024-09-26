import pandas as pd
from fuzzywuzzy import fuzz, process
import msoffcrypto
import io


# Load the Excel files
file1 = 'X:/Data/YuTing/Project/Tabular/ViewCatalog/BCWomen_ViewCount_2023-11-04.xlsx'
file2 = 'X:/Data/YuTing/Project/Tabular/XWalk/XW_Kheiron13Feb2024.xlsx'
password = 'BDenCrossWalk'

# Open and decrypt the password-protected file
decrypted = io.BytesIO()
with open(file2, 'rb') as f:
    office_file = msoffcrypto.OfficeFile(f)
    office_file.load_key(password=password)  # Load the password
    office_file.decrypt(decrypted)  # Decrypt the file into an in-memory buffer

df1 = pd.read_excel(file1, sheet_name=None) #Load all sheets
df2 = pd.read_excel(decrypted)

# Clean and standardize the columns
def clean_column(df, column):
    df[column] = df[column].astype(str).str.strip().str.lower().replace('nan', None)
    return df

df2 = clean_column(df2, 'BDProjectID')
df2['StudyDate'] = pd.to_datetime(df2['StudyDate'])
df2['AccessionNum'] = df2['AccessionNum'].fillna('')  # Handle missing AccessionNumbers

# Initialize result lists
matched_list = []
mismatched_list = []
similar_studies = []

# Iterate over each sheet in df1_sheets
for sheet_name, df1 in df1.items():
    print(f"Processing sheet: {sheet_name}")
    
    # Clean and standardize the columns in df1
    df1 = clean_column(df1, 'patient_id')
    df1['StudyDate'] = pd.to_datetime(df1['StudyDate'])
    df1['AccessionNumber'] = df1['AccessionNumber'].fillna('')  # Handle missing AccessionNumbers
    
    # Matching process
    for index1, row1 in df1.iterrows():
        # Exact matching by patient_id, StudyDate, and AccessionNumber
        if row1['AccessionNumber']:  # If AccessionNumber is available
            match = df2[(df2['BDProjectID'] == row1['patient_id']) & 
                        (df2['StudyDate'] == row1['StudyDate']) & 
                        (df2['AccessionNum'] == row1['AccessionNumber'])]
        else:  # If AccessionNumber is missing, match by patient_id and StudyDate only
            match = df2[(df2['BDProjectID'] == row1['patient_id']) & 
                        (df2['StudyDate'] == row1['StudyDate'])]
        
        # If exact match is found
        if not match.empty:
            matched_list.append((row1['patient_id'], row1['StudyDate'], row1['AccessionNumber'], match.iloc[0]['AccessionNum'], sheet_name))
        else:
            # If no exact match, try to find similar studies using fuzzy matching on AccessionNumber
            if row1['AccessionNumber']:
                similar_accession = process.extractOne(row1['AccessionNumber'], df2['AccessionNum'], scorer=fuzz.token_sort_ratio)
                if similar_accession and similar_accession[1] > 80:  # Adjust threshold for similarity
                    similar_match = df2[df2['AccessionNum'] == similar_accession[0]]
                    if not similar_match.empty:
                        similar_studies.append((row1['patient_id'], row1['StudyDate'], row1['AccessionNumber'], similar_accession[0], sheet_name))
                        continue

            # If no similar match, add to mismatched list
            mismatched_list.append((row1['patient_id'], row1['StudyDate'], row1['AccessionNumber'], sheet_name))

# Convert the result lists to DataFrames
matched_df = pd.DataFrame(matched_list, columns=['patient_id', 'StudyDate', 'AccessionNumber_file1', 'AccessionNum_file2', 'Sheet'])
mismatched_df = pd.DataFrame(mismatched_list, columns=['patient_id', 'StudyDate', 'AccessionNumber', 'Sheet'])
similar_studies_df = pd.DataFrame(similar_studies, columns=['patient_id', 'StudyDate', 'AccessionNumber_file1', 'Similar_AccessionNum_file2', 'Sheet'])

# Save results to Excel
matched_df.to_excel('matched_list.xlsx', index=False)
mismatched_df.to_excel('mismatched_list.xlsx', index=False)
similar_studies_df.to_excel('similar_studies.xlsx', index=False)

print("Results saved to Excel files.")