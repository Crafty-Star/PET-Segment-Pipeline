import os
import nibabel as nib
import gzip
import shutil
#from moosez import moose

#helper functions
def safe_remove(    inpute_delete):
    try:
        os.path.exists(inpute_delete)
        os.remove(inpute_delete)
    except OSError:
        print("Error: %s - %s." % (inpute_delete, os.strerror))

#get the input directory from the user or use the default
input_dir = 'C:\\Users\\GreyS\\Desktop\\Pleat'
input_dir_from_user = input("Enter the path to the input directory with PET scans: ")
if input_dir_from_user=="":
    input_dir = input_dir
else:
    input_dir = input_dir_from_user

#get a list of folders (for each patients) in the input folder
files_dir = [    f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))]


#for each patient convert gz files and DICOM files to nifti files and rename them as PT_patient.nii
for patient in files_dir:
    files_file = [f for f in os.listdir(input_dir+'\\'+patient) if os.path.isfile(os.path.join(input_dir+'\\'+patient, f))]
    itr = 0
    for scan in files_file:
        print(input_dir+'\\'+patient+'\\'+scan)
        # scan = Path to the input .nii.gz file
        if scan.endswith(".gz"):
            # Path to unzipped file
            input_scan = input_dir+'\\'+patient+'\\'+scan
            # Path to save the output .nii file
            output_scan = input_dir+'\\'+patient+'\\'+'PT_'+patient+str(itr)+'.nii'
            #p Path to save the temporary unzipped file
            temp_file = input_dir+'\\'+patient+'\\'+'temp.nii'
            # Unzip the .nii.gz file
            with gzip.open(input_scan, 'rb') as f_in:
                with open(temp_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # Load the .nii file using nibabel
            img = nib.load(temp_file)
            # Save the file as .nii
            nib.save(img, output_scan)
            # Remove the temporary file
            os.remove(temp_file)
            print(f"File saved as {output_scan}")
            #remove the gz file
            safe_remove(input_scan)
            itr+=1


#begin the segmentation
os.system("moosez -d C:\\Users\\GreyS\\Desktop\\Pleat -m clin_pt_fdg_brain_v1")


#variables for the moosez function
#model_name = 'clin_pt_fdg_brain_v1'
#input_dir = 'C:\\Users\\GreyS\\Desktop\\Pleat'
#output_dir = 'C:\\Users\\GreyS\\Desktop\\Mooze_output'
#accelerator = 'cpu'
#broken for some reason
#moose(model_name, input_dir, output_dir, accelerator)x