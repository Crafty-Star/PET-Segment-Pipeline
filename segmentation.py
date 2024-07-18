import os
import nibabel as nib
import gzip
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import sys
#from moosez import moose

#helper functions
def safe_remove(inpute_delete):
    try:
        os.path.exists(inpute_delete)
        os.remove(inpute_delete)
    except OSError:
        print("Error: %s - %s." % (inpute_delete, os.strerror))
def ensure_prefix(s):
    if not s.startswith("PT_"):
        s = "PT_" + s
    return s
import os
def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File renamed from {old_name} to {new_name}")
    except FileNotFoundError:
        print(f"The file {old_name} does not exist")
    except PermissionError:
        print(f"Permission denied to rename {old_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('No directory selected', self)
        layout.addWidget(self.label)

        self.btnChooseDir = QPushButton('Choose Directory', self)
        self.btnChooseDir.clicked.connect(self.showDialog)
        layout.addWidget(self.btnChooseDir)

        self.btnRunFunction = QPushButton('Run Segmentation', self)
        self.btnRunFunction.clicked.connect(self.runSegmentation)
        layout.addWidget(self.btnRunFunction)

        self.setLayout(layout)

        self.setWindowTitle('Basic PyQt5 GUI')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def showDialog(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.label.setText(f'Selected Directory: {directory}')
            self.selected_directory = directory

    def runFunction(self):
        # Replace this function with your actual function
        if hasattr(self, 'selected_directory'):
            print(f'Running function on: {self.selected_directory}')
        else:
            print('No directory selected')
            
    def runSegmentation(self):
        #get a list of folders (for each patients) in the input folder
        files_dir = [    f for f in os.listdir(self.selected_directory) if os.path.isdir(os.path.join(self.selected_directory, f))]

        #for each patient convert gz files and DICOM files to nifti files and rename them as PT_patient.nii
        for patient in files_dir:
            files_file = [f for f in os.listdir(self.selected_directory+'\\'+patient) if os.path.isfile(os.path.join(self.selected_directory+'\\'+patient, f))]
            itr = 0
            for scan in files_file:
                #print(self.selected_directory+'\\'+patient+'\\'+scan)
                # scan = Path to the input .nii.gz file
                if scan.endswith(".gz"):
                    # Path to unzipped file
                    input_scan = self.selected_directory+'\\'+patient+'\\'+scan
                    # Path to save the output .nii file
                    output_scan = self.selected_directory+'\\'+patient+'\\'+'PT_'+patient+"_"+str(itr)+'.nii'
                    # Path to save the temporary unzipped file
                    temp_file = self.selected_directory+'\\'+patient+'\\'+'temp.nii'
                    # Unzip the .nii.gz file
                    with gzip.open(input_scan, 'rb') as f_in:
                        with open(temp_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    # Load the .nii file using nibabel
                    img = nib.load(temp_file)
                    # Save the file as .nii
                    nib.save(img, output_scan)
                    # Remove the temporary file
                    safe_remove(temp_file)
                    #print(f"File saved as {output_scan}")
                    #remove the gz file
                    safe_remove(input_scan)
                    itr+=1
                elif scan.endswith(".nii"):
                    # Path to unzipped file
                    input_scan = self.selected_directory+'\\'+patient+'\\'+scan
                    corrected_scan = self.selected_directory+'\\'+patient+'\\'+ensure_prefix(scan)
                    # Adds the "PT_" prefix to the filename if not there
                    os.rename(input_scan,corrected_scan)
        #begin the segmentation
        os.system("moosez -d C:\\Users\\GreyS\\Desktop\\Pleat -m clin_pt_fdg_brain_v1")
        print("Segmentation Complete")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#variables for the moosez function
#model_name = 'clin_pt_fdg_brain_v1'
#input_dir = 'C:\\Users\\GreyS\\Desktop\\Pleat'
#output_dir = 'C:\\Users\\GreyS\\Desktop\\Mooze_output'
#accelerator = 'cpu'
#broken for some reason
#moose(model_name, input_dir, output_dir, accelerator)x