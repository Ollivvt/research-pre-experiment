import pandas as pd

def clean_patient_data(input_file, selected_columns):
    # Step 1: Read the CSV file
    try:
        df = pd.read_csv(input_file, low_memory=False)
        print(f"Total records in original dataset: {len(df)}")
        print(f"Total unique patients in original dataset: {df['phn'].nunique()}")
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None, None, None
    
    # Step 2: Validate required columns are present
    required_cols = ['phn', 'birth_ctry_code', 'birth_ctry_text', 'ethnicity'] + selected_columns
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Step 3: Preprocess and clean data
    # Ensure 'phn' is not null
    df = df[df['phn'].notna()]
    
    # Step 4: Group by `phn` and process each patient
    matched_records = []
    unmatched_records = []
    
    grouped = df.groupby('phn')
    
    for phn, group in grouped:
        # Check if any record has valid values in 'birth_ctry_code', 'birth_ctry_text', or 'ethnicity'
        has_valid_info = group[
            (group['birth_ctry_code'].notna() & (group['birth_ctry_code'] != 'U')) |
            (group['birth_ctry_text'].notna() & (group['birth_ctry_text'] != 'U')) |
            (group['ethnicity'].notna() & (group['ethnicity'] != 'U'))
        ]
        
        if not has_valid_info.empty:
            # If at least one valid record exists, include the patient in matched list
            # Select one valid record (or more if needed) for matched
            valid_records = has_valid_info[selected_columns]
            matched_records.extend(valid_records.to_dict('records'))
        else:
            # If no valid records exist, add all records to unmatched list
            unmatched_records.extend(group.to_dict('records'))
    
    # Step 5: Convert unmatched to DataFrame and identify unique patients without valid fields
    unmatched_df = pd.DataFrame(unmatched_records) if unmatched_records else pd.DataFrame()
    ethnicity_missing_records = unmatched_df[
        (unmatched_df['birth_ctry_code'].isna() | (unmatched_df['birth_ctry_code'] == 'U')) &
        (unmatched_df['birth_ctry_text'].isna() | (unmatched_df['birth_ctry_text'] == 'U')) &
        (unmatched_df['ethnicity'].isna() | (unmatched_df['ethnicity'] == 'U'))
    ]
    unique_ethnicity_missing_patients = ethnicity_missing_records['phn'].nunique()
    
    # Step 6: Select only specified columns for output
    ethnicity_missing_records = ethnicity_missing_records[selected_columns].drop_duplicates(subset='phn')
    matched_records = pd.DataFrame(matched_records)[selected_columns].drop_duplicates(subset='phn')

    # Reporting
    print(f"Total unique matched patients: {matched_records['phn'].nunique()}")
    print(f"Total unique patients without ethnicity: {unique_ethnicity_missing_patients}")
    
    return matched_records, ethnicity_missing_records

def main():
    # Input file path
    input_file = r'U:\GitHub\research-pre-experiment\Mammo\Screening Registry.csv'
    
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
    matched, ethnicity_missing = clean_patient_data(input_file, selected_columns)
    
    # Save results
    if matched is not None and not matched.empty:
        matched.to_csv('matched_patient_records.csv', index=False)
        print("Matched records saved.")
    
    if ethnicity_missing is not None and not ethnicity_missing.empty:
        ethnicity_missing.to_csv('ethnicity_missing.csv', index=False)
        print("Ethnicity missing records saved.")

# Ensure the script can be run directly or imported
if __name__ == '__main__':
    main()
