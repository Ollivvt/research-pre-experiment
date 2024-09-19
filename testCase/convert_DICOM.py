import pydicom
import matplotlib.pyplot as plt

# Load the DICOM file
dicom_file_path = 'MG_RCC_Processed.dcm'  # Update with the actual file path
dicom_data = pydicom.dcmread(dicom_file_path)

# Extract basic information from the DICOM file
dicom_info = {
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

# Print the extracted information
for key, value in dicom_info.items():
    print(f"{key}: {value}")

'''
Matplotlib - shows the image
'''
# Extract the pixel array
img_array = dicom_data.pixel_array

# Display the image
plt.imshow(img_array, cmap='gray')
plt.show()