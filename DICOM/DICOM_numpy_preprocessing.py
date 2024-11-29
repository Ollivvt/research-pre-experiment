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

def preprocess_dicom_images_to_numpy(input_folder, img_size=IMG_SIZE):
    """Preprocess DICOM images in subfolders and store them as a NumPy array."""
    # Recursively find all DICOM files in the input folder and its subfolders
    dicom_files = glob(os.path.join(input_folder, '**/*.dcm'), recursive=True)
    
    preprocessed_images = []
    
    for dicom_file in dicom_files:
        # Load and preprocess the DICOM image
        img = load_dicom_image(dicom_file)
        resized_img = resize_image(img, size=img_size)
        
        # Append the processed image to the list
        preprocessed_images.append(resized_img)
        
        print(f"Processed: {dicom_file}")
    
    # Convert the list of images to a NumPy array
    preprocessed_images_np = np.array(preprocessed_images)
    
    return preprocessed_images_np

# Example usage
if __name__ == "__main__":
    # Preprocess images and get them as a NumPy array
    preprocessed_images_np = preprocess_dicom_images_to_numpy(input_root_folder)
    
    # Save the NumPy array for later use
    np.save(output_folder, preprocessed_images_np)
    print(f"Saved preprocessed images as a NumPy array: {output_folder}")
