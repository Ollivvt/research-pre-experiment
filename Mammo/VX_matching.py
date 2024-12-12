import pandas as pd
from fuzzywuzzy import fuzz, process
import msoffcrypto
import io

# Load the Excel files
file1 = 'D:/Data/YuTing/Project/Tabular/ViewCatalog/Burnaby_ViewCount_2023-11-03.xlsx'
file2 = 'D:/Data/YuTing/Project/Tabular/XWalk/XW_Kheiron13Feb2024.xlsx'
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

# Handle StudyDate as a string for comparison
def studydate_as_numeric(df, date_column):
    df[date_column] = df[date_column].astype(str).str.strip()  # Keep as numeric string format

# Check for invalid AccessionNumber
def validate_accession_number(accession):
    if '-' in str(accession):
        return None  # Treat as missing
    return str(accession)

# Apply cleaning and validation
df2 = clean_column(df2, 'BDProjectID')
studydate_as_numeric(df2, 'StudyDate')
df2['AccessionNum'] = df2['AccessionNum'].apply(validate_accession_number)
df2['InstitutionName'] = df2['InstitutionName']

# Initialize result lists
matched_list = []
mismatched_list = []

# Iterate over each sheet in df1_sheets
for sheet_name, df1 in df1.items():
    print(f"Processing sheet: {sheet_name}")
    
    # Clean and standardize the columns in df1
    df1 = clean_column(df1, 'patient_id')
    studydate_as_numeric(df1, 'StudyDate')
    df1['AccessionNumber'] = df1['AccessionNumber'].fillna('')  # Handle missing AccessionNumbers
    df1['InstitutionName'] = df1['InstitutionName'].fillna('')  # Handle missing InstitutionName
    df1['Manufacturer'] = df1['Manufacturer'].fillna('') # Handle missing Manufacturer
    
    # Matching process
    for index1, row1 in df1.iterrows():
        # First, try to match by patient_id, StudyDate (in numeric form), and AccessionNumber (if available)
        if row1['AccessionNumber']:
            match = df2[(df2['BDProjectID'] == row1['patient_id']) & 
                        (df2['StudyDate'] == row1['StudyDate']) & 
                        (df2['AccessionNum'] == row1['AccessionNumber'])]
        else:
            # If AccessionNumber is not available, only match on patient_id and StudyDate (in numeric form)
            match = df2[(df2['BDProjectID'] == row1['patient_id']) & 
                        (df2['StudyDate'] == row1['StudyDate'])]
        '''
        match = df2[(df2['BDProjectID'] == row1['patient_id']) & 
                        (df2['StudyDate'] == row1['StudyDate'])]
        '''
        # If exact match is found, include only one AccessionNumber
        if not match.empty:
            matched_list.append((row1['patient_id'], row1['StudyDate'], row1['AccessionNumber'], sheet_name))
        else:
            # Separate checks for mismatches on patient_id and AccessionNumber (StudyDate is only secondary)
            accession_mismatch = False
            patientid_mismatch = False

            # Check for patient_id mismatch (based on StudyDate match in numeric form)
            match_without_patientid = df2[(df2['StudyDate'] == row1['StudyDate']) & (df2['AccessionNum'] == row1['AccessionNumber'])]
            if not match_without_patientid.empty:
                if match_without_patientid['BDProjectID'].iloc[0] != row1['patient_id']:
                    patientid_mismatch = True

            # Check for AccessionNumber mismatch if AccessionNumber exists
            if row1['AccessionNumber']:
                match_without_accession = df2[(df2['BDProjectID'] == row1['patient_id']) & (df2['StudyDate'] == row1['StudyDate'])]
                if not match_without_accession.empty:
                    if match_without_accession['AccessionNum'].iloc[0] != row1['AccessionNumber']:
                        accession_mismatch = True
            
            # Record the mismatch type if there is no fuzzy match
            if not patientid_mismatch and not accession_mismatch:
                mismatched_list.append(('', row1['patient_id'], '', row1['StudyDate'], '', row1['AccessionNumber'], '', row1['InstitutionName'],'', '', sheet_name))
            else:
                # If any mismatch exists, record it in a more detailed manner
                if accession_mismatch and not match_without_accession.empty:
                    mismatched_list.append(('AccessionNumber Mismatch', 
                                            row1['patient_id'], match_without_accession['BDProjectID'].iloc[0],
                                            row1['StudyDate'], match_without_accession['StudyDate'].iloc[0],
                                            row1['AccessionNumber'], match_without_accession['AccessionNum'].iloc[0], 
                                            row1['InstitutionName'], match_without_accession['InstitutionName'].iloc[0], 
                                            row1['Manufacturer'], sheet_name))
                if patientid_mismatch and not match_without_patientid.empty:
                    mismatched_list.append(('PatientID Mismatch', 
                                            row1['patient_id'], match_without_patientid['BDProjectID'].iloc[0],
                                            row1['StudyDate'], match_without_patientid['StudyDate'].iloc[0],
                                            row1['AccessionNumber'], match_without_patientid['AccessionNum'].iloc[0], 
                                            row1['InstitutionName'], match_without_patientid['InstitutionName'].iloc[0], 
                                            row1['Manufacturer'], sheet_name))

# Convert the result lists to DataFrames			
matched_df = pd.DataFrame(matched_list, columns=['patient_id', 'StudyDate', 'AccessionNumber', 'Sheet'])			
mismatched_df = pd.DataFrame(mismatched_list, columns=['Mismatch_Reason',			
                                                       'patient_id_file1', 'patient_id_file2', 'StudyDate_file1', 'StudyDate_file2',			
                                                       'AccessionNumber_file1', 'AccessionNumber_file2', 
                                                       'InstitutionName_file1', 'InstitutionName_file2', 
                                                       'Manufacturer_file1', 'Sheet'])			


# Save results to Excel
matched_df.to_excel('Burnaby_matched_list.xlsx', index=False)
mismatched_df.to_excel('Burnaby_mismatched_list.xlsx', index=False)

print("Results saved to Excel files.")
