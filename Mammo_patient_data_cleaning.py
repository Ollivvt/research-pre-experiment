import pandas as pd
import numpy as np

def clean_patient_data(input_file, selected_columns):
    # Step 1: Read the Excel file
    try:
        df = pd.read_excel(input_file)
        print(f"Total records in original dataset: {len(df)}")
        print(f"Total unique patients in original dataset: {df['phn'].nunique()}")
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None, None, None
    
    # Step 2: Validate required columns are present
    required_cols = ['phn', 'last_name', 'first_name', 'date_of_birth', 
                     'birth_ctry_code', 'birth_ctry_text', 'ethnicity'] + selected_columns
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Step 3: Preprocess and clean data
    # Convert names to uppercase and remove extra whitespace
    df['last_name'] = df['last_name'].str.strip().str.upper()
    df['first_name'] = df['first_name'].str.strip().str.upper()
    
    # Step 4: Group by patient identifiers
    grouped = df.groupby(['phn', 'last_name', 'first_name', 'date_of_birth'])
    
    # Lists to store matched, unmatched, and ethnicity missing records
    matched_records = []
    unmatched_records = []
    ethnicity_missing_records = []
    
    # Step 5: Process each patient group
    for (phn, last_name, first_name, dob), group in grouped:
        # Check if group has consistent records
        unique_birth_ctry_code = group['birth_ctry_code'].nunique()
        unique_birth_ctry_text = group['birth_ctry_text'].nunique()
        unique_ethnicity = group['ethnicity'].nunique()
        
        # Prepare selected columns for this group
        group_selected = group[selected_columns]
        
        # If all records are consistent
        if unique_birth_ctry_code == 1 and unique_birth_ctry_text == 1 and unique_ethnicity == 1:
            # Select the first record (all are identical)
            matched_record = group_selected.iloc[0].copy()
            matched_record['record_count'] = len(group)
            matched_records.append(matched_record)
        else:
            # Add all records to unmatched if inconsistencies exist
            for _, record in group_selected.iterrows():
                record_copy = record.copy()
                record_copy['inconsistency_reason'] = (
                    f"Inconsistent records: "
                    f"Birth Country Code Variations: {unique_birth_ctry_code}, "
                    f"Birth Country Text Variations: {unique_birth_ctry_text}, "
                    f"Ethnicity Variations: {unique_ethnicity}"
                )
                unmatched_records.append(record_copy)
    
    # Step 6: Identify records without ethnicity info
    # From unmatched records and original dataset
    df_unmatched = pd.DataFrame(unmatched_records) if unmatched_records else pd.DataFrame()
    
    # Combine unmatched and paired records to find those without ethnicity
    all_processed_phn = set(pd.DataFrame(matched_records)['phn'] if matched_records else [])
    
    if not df_unmatched.empty:
        unmatched_phn = set(df_unmatched['phn'])
    else:
        unmatched_phn = set()
    
    # Find patients without ethnicity in the original dataset
    ethnicity_missing = df[
        (~df['phn'].isin(all_processed_phn)) & 
        (~df['phn'].isin(unmatched_phn)) & 
        (df['ethnicity'].isna() | (df['ethnicity'] == ''))
    ]
    
    # Select only the specified columns for ethnicity missing records
    ethnicity_missing_records = ethnicity_missing[selected_columns]
    
    # Reporting
    print(f"Total matched patient records: {len(matched_records)}")
    print(f"Total unmatched patient records: {len(unmatched_records)}")
    print(f"Patients without ethnicity information: {len(ethnicity_missing_records)}")
    
    # Convert lists to DataFrames
    matched_df = pd.DataFrame(matched_records) if matched_records else pd.DataFrame()
    unmatched_df = pd.DataFrame(unmatched_records) if unmatched_records else pd.DataFrame()
    
    return matched_df, unmatched_df, ethnicity_missing_records

def main():
    # Input file path (replace with your actual file path)
    input_file = r'H:\Early Detection\Group\1 Breast Cancer Risks in Early Detection and Prevention\AI Ethnicity\Data\Mammo\ScreeningRegistry\rasika_kheiron_reflections+cascade_combined_corrected_20230725.xlsx'
    
    # Specify the columns you want to save
    selected_columns = [
        'phn', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 
        'clinic_code', 'clinic_name', 'screen_date', 'data_source', 
        'height_cm', 'birth_ctry_code', 'birth_ctry_text', 'ethnicity', 
        'educ_code', 'educ_text', 'age_at_menarche', 
        'num_full_term_deliveries', 'age_at_1st_delivery', 
        'menstruating_flag', 'age_menstruation_stopped', 
        'weight_kg', 'mammo_density_cd', 'mammo_density_text'
    ]
    
    # Clean the data
    matched, unmatched, ethnicity_missing = clean_patient_data(input_file, selected_columns)
    
    # Save results
    if matched is not None and not matched.empty:
        matched.to_csv('mammoPatient/matched_patient_records.csv', index=False)
        print("Matched records saved.")
    
    if unmatched is not None and not unmatched.empty:
        unmatched.to_csv('mammoPatient/unmatched_patient_records.csv', index=False)
        print("Unmatched records saved.")
    
    if ethnicity_missing is not None and not ethnicity_missing.empty:
        ethnicity_missing.to_csv('mammoPatient/ethnicity_missing.csv', index=False)
        print("Ethnicity missing records saved.")

# Ensure the script can be run directly or imported
if __name__ == '__main__':
    main()
