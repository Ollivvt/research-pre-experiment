import os
import pydicom
import csv

def find_dicom_files(root_dir):
    """
    Recursively find all DICOM files in a directory and its subdirectories.
    Args:
        root_dir (str): Root directory where DICOM files are located.

    Returns:
        list: List of paths to DICOM files.
    """
    dicom_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".dcm"):
                dicom_files.append(os.path.join(dirpath, file))
    return dicom_files

def extract_dicom_metadata(dicom_file):
    """
    Extract relevant metadata from a DICOM file.
    Args:
        dicom_file (str): Path to a DICOM file.

    Returns:
        dict: Extracted metadata.
    """
    try:
        dicom_data = pydicom.dcmread(dicom_file)
        metadata = {
            "File": dicom_file,
            "PatientID": dicom_data.get("PatientID", "N/A"),
            "PatientName": dicom_data.get("PatientName", "N/A"),
            "PatientAge": dicom_data.get("PatientAge", "N/A"),
            "PatientSex": dicom_data.get("PatientSex", "N/A"),
            "StudyDate": dicom_data.get("StudyDate", "N/A"),
            "Modality": dicom_data.get("Modality", "N/A"),
            "BodyPartExamined": dicom_data.get("BodyPartExamined", "N/A"),
            "ViewPosition": dicom_data.get("ViewPosition", "N/A"),
            "Manufacturer": dicom_data.get("Manufacturer", "N/A"),
            "Rows": dicom_data.get("Rows", "N/A"),
            "Columns": dicom_data.get("Columns", "N/A")
        }
        return metadata
    except Exception as e:
        print(f"Error reading {dicom_file}: {e}")
        return None

def save_metadata_to_csv(metadata_list, output_csv):
    """
    Save the extracted metadata to a CSV file.
    Args:
        metadata_list (list): List of dictionaries containing metadata.
        output_csv (str): Output path for the CSV file.
    """
    with open(output_csv, mode='w', newline='') as csvfile:
        fieldnames = ["File", "PatientID", "PatientName", "PatientAge", "PatientSex", 
                      "StudyDate", "Modality", "BodyPartExamined", "ViewPosition", 
                      "Manufacturer", "Rows", "Columns"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for metadata in metadata_list:
            if metadata:
                writer.writerow(metadata)

def process_dicom_files_and_save_csv(root_directory, output_csv):
    """
    Process all DICOM files in the directory, extract metadata, and save to CSV.
    Args:
        root_directory (str): Root directory containing DICOM files.
        output_csv (str): Path to the output CSV file.
    """
    dicom_files = find_dicom_files(root_directory)
    metadata_list = []
    
    for dicom_file in dicom_files:
        metadata = extract_dicom_metadata(dicom_file)
        if metadata:
            metadata_list.append(metadata)
    
    save_metadata_to_csv(metadata_list, output_csv)
    print(f"Metadata extracted and saved to {output_csv}")

# Set the root directory and output CSV file
root_directory = r"\\205.233.161.11\ai-primary3\AIRM\BCWomen\BDenStorage\Diagnostic\20130116\20190906_7cpdmf\20130116_MG Diagnostic RT"  # Example: "/path/to/dicom/files"
output_csv = "dicom_metadata.csv"

# Run the script to process DICOM files and save metadata to CSV
process_dicom_files_and_save_csv(root_directory, output_csv)
