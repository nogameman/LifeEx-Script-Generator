import os

def get_patient_ids(folder_path, prefix, suffix):
    """
    Extract patient IDs from filenames in the specified folder.
    
    Args:
    folder_path (str): Path to the folder containing the files.
    prefix (str): Prefix of the filenames.
    suffix (str): Suffix of the filenames.
    
    Returns:
    list: Sorted list of patient IDs.
    """
    patients = []
    for filename in os.listdir(folder_path):
        if filename.startswith(prefix) and filename.endswith(suffix):
            patient_id = filename[len(prefix):-len(suffix)]
            patients.append(patient_id)
    patients.sort()
    return patients

def write_to_files(output_path, patients, folder_image, folder_roi, file_suffix, op_template):
    """
    Write configuration scripts for images and ROIs.
    
    Args:
    output_path (str): Path to the output configuration file.
    patients (list): List of patient IDs.
    folder_image (str): Path to the folder containing the image files.
    folder_roi (str): Path to the folder containing the ROI files.
    file_suffix (str): Suffix of the image filenames.
    op_template (str): Template string for operation configuration.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as file:
        file.write("# LIFEx.Output.Directory=" + output_path.replace('\\', '/') + "\n\n")
        for index, patient_id in enumerate(patients):
            image_path = os.path.join(folder_image, f'{patient_id}{file_suffix}').replace('\\', '/')
            roi_path = os.path.join(folder_roi, f'binary_{patient_id}_roi.nii.gz').replace('\\', '/')
            
            file.write(f'LIFEx.Patient{index}.Series0={image_path}\n')
            file.write(op_template.format(index))
            file.write(f'LIFEx.Patient{index}.Roi0={roi_path}\n\n')

def main():
    # Environment variables or default paths
    folder_image = os.getenv('FOLDER_IMAGE', 'images')
    folder_roi = os.getenv('FOLDER_ROI', 'rois')
    output_path = os.getenv('OUTPUT_PATH', 'output/config.txt')
    file_suffix = os.getenv('FILE_SUFFIX', '_image.nii.gz')
    
    # Documentation for op_template:
    # The op_template variable defines the operations to be performed on the images.
    # It uses a placeholder for the patient index and can be customized to include various parameters:
    #   - Operation type: 'Texture' in this case.
    #   - Boolean flags: For specific operation settings (e.g., true, false, false).
    #   - Dimension: '3d' for 3D operations.
    #   - Method: 'RelativeMinMax' for relative min-max normalization.
    #   - Bin width: The second-to-last parameter (e.g., 8.0).
    # Adjust the bin width as needed.
    bin_width = os.getenv('BIN_WIDTH', '8.0')
    op_template = f'LIFEx.Patient{{}}.Series0.Operation0=Texture,true,false,false,1,3d,RelativeMinMax,{bin_width},0.0\n'
    
    patients = get_patient_ids(folder_roi, 'binary_', '_roi.nii.gz')
    
    write_to_files(output_path, patients, folder_image, folder_roi, file_suffix, op_template)

if __name__ == "__main__":
    main()
