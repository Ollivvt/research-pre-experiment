import pandas as pd
import os

def filter_patients_by_ethnicity(input_file, output_file):
    try:
        # Read the matched records file
        df = pd.read_csv(input_file)
        print(f"Total records in matched dataset: {len(df)}")
        
        # Filter records where ethnicity is not 'U'
        filtered_df = df[
            (df['ethnicity'].notna()) & (df['ethnicity'] != 'U')
        ]
        
        print(f"Total records after filtering: {len(filtered_df)}")
        
        # Save filtered records to the output file
        filtered_df.to_csv(output_file, index=False)
        print(f"Filtered records saved to {output_file}")
    
    except Exception as e:
        print(f"Error processing the file: {e}")

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_file = os.path.join(script_dir, 'outputs', 'mammoPatient', 'matched_patient_records.csv')
    output_file = os.path.join(script_dir, 'outputs', 'mammoPatient', 'ethnicity_patient_records.csv')
    
    # Filter the patients
    filter_patients_by_ethnicity(input_file, output_file)

if __name__ == '__main__':
    main()
