import os
import pydicom
import numpy as np
import cv2
from glob import glob

# DICOM root folder (containing subfolders)
input_root_folder = r"\\205.233.161.11\ai-primary3\AIRM\BCWomen\BDenStorage\Diagnostic"
output_folder = 'Z:/Images/DICOM_preprocessing_224'

# Desired image size (adjustable depending on the model)
IMG_SIZE = 224  # Can also try 512 or 1024 based on your model and hardware

def load_dicom_image(dicom_path):
    """Load and process a single DICOM image."""
    try:
        dicom = pydicom.dcmread(dicom_path)
        img = dicom.pixel_array.astype(np.float32)
        img = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX)  # Normalize to [0, 1]
        return img
    except Exception as e:
        print(f"Error loading DICOM file {dicom_path}: {e}")
        return None

def resize_image(image, size=IMG_SIZE):
    """Resize image to the specified size."""
    if image is None:
        return None
    return cv2.resize(image, (size, size), interpolation=cv2.INTER_LINEAR)

def preprocess_dicom_images_in_subfolders(input_folder, output_folder, img_size=IMG_SIZE):
    """Preprocess DICOM images in subfolders and save them as PNG."""
    # Recursively find all DICOM files in the input folder and its subfolders
    dicom_files = glob(os.path.join(input_folder, '**/*.dcm'), recursive=True)
    
    for dicom_file in dicom_files:
        # Load and preprocess the DICOM image
        img = load_dicom_image(dicom_file)
        resized_img = resize_image(img, size=img_size)
        
        # Create a corresponding subfolder structure in the output folder
        relative_path = os.path.relpath(dicom_file, input_folder)
        output_subfolder = os.path.dirname(relative_path)
        output_path = os.path.join(output_folder, output_subfolder)
        
        # Ensure the output subfolder exists
        os.makedirs(output_path, exist_ok=True)
        
        # Save the processed image as PNG
        filename = os.path.basename(dicom_file).replace('.dcm', '.png')
        output_filepath = os.path.join(output_path, filename)
        
        # Convert to 8-bit for saving as PNG
        final_img = (resized_img * 255).astype(np.uint8)
        cv2.imwrite(output_filepath, final_img)
        
        print(f"Saved: {output_filepath}")

# Example usage
if __name__ == "__main__":
    preprocess_dicom_images_in_subfolders(input_root_folder, output_folder)
