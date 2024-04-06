![OpenMAP_Logo_with_name](https://github.com/OishiLab/OpenMAP-T1/assets/64403395/9ce68146-eeb7-4ce0-bd49-73f1c7ded4d8)

# OpenMAP-Di
**OpenMAP-Di parcellates an infant's DTI brain scan into 169 anatomical regions.**

## System Requirements
### Operating System
OpenMAP-Di has been tested on Linux (Ubuntu 22.04) and MacOS. Although untested, it should theoretically work on Windows as well.
### Hardware Requirements
Like the [nnU-Net hardware requirements for inference](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md#hardware-requirements-for-inference), a GPU of at least 4 GB of available VRAM is recommended for faster predictions; however, inference times are typically still manageable on CPU and MPS (Apple M1/M2).

## Installation Instructions
0. Create a Python 3 virtual environment. Activate the environment.
```
conda create -n OpenMAP-Di python=3.10
conda activate OpenMAP-Di
```

1. Clone this repository.
```
git clone https://github.com/OishiLab/OpenMAP-Di.git
cd OpenMAP-Di
```

2. Install the required Python libraries.
```
pip install -r requirements.txt
```

3. Download the pre-trained model using this link. [Link of pretraind model!](https://forms.office.com/Pages/ResponsePage.aspx?id=OPSkn-axO0eAP4b4rt8N7Iz6VabmlEBIhG4j3FiMk75UNkxFRk5IRkY3MjJaNU9POUZBNlNQRzUxVy4u)

4. Convert the data you would like to parcellate into the [nnU-Net data format for inference](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_format_inference.md). Specifically, the `INPUT_FOLDER` should look similar to below. Channel numbers are defined in the `dataset.json` file within the pre-trained `MODEL_FOLDER`; for the provided model, channels `0000`, `0001`, `0002`, `0003`, `0004` correspond to `dwi`, `b0`, `color_r`, `color_g`, `color_b`. `convert_to_nnunet_format.py` has also been provided to assist in the conversion; see help (`-h`) for more details.
```
python convert_to_nnunet_format.py -i INPUT_FOLDER -d DWI_FILE -b B0_FILE -c COLOR_FILE -s SUBJECT_IDENTIFIER
```
        INPUT_FOLDER
        ├── brain_00_0000.nii.gz
        ├── brain_00_0001.nii.gz
        ├── brain_00_0002.nii.gz
        ├── brain_00_0003.nii.gz
        ├── brain_00_0004.nii.gz
        ├── brain_01_0000.nii.gz
        ├── brain_01_0001.nii.gz
        ├── brain_01_0002.nii.gz
        ├── brain_01_0003.nii.gz
        ├── brain_01_0004.nii.gz
        ├── ...

5. Run `parcellate_neonatal_brain.py` to parcellate your dataset! See help (`-h`) for more details. Inferred parcellations will be outputted to the `OUTPUT_FOLDER`, while postprocessed parcellations will be outputted to a `postprocessing` subfolder of the `OUTPUT_FOLDER`.
```
python parcellate_neonatal_brain.py -i INPUT_FOLDER -o OUTPUT_FOLDER -m MODEL_FOLDER -device DEVICE
```

## Citation
In recognition of the efforts put into developing the OpenMAP-Di model, you are required to cite the model appropriately in any publications, presentations, or research outputs that utilize this model. This citation is crucial for acknowledging the work of the developers and contributing to the academic and professional discourse surrounding deep learning and its applications.
[Kengo Onda, Nathanael Kuo, Kei Nishimaki, Jill Chotiyanonta, Yukako Kawasaki, Linda Chang, Thomas Ernst, Charlamaine Parkinson, Aylin Tekes, Raul Chavez-Valdez, Dhananjay Vaidya, Ernest M. Graham, Allen D. Everett, Frances J. Northington, and Kenichi Oishi. OpenMAP-Di: Open Resource for Multiple Anatomical Region Parcellation of Diffusion MRI for Infantile Hypoxic-Ischemic Lesion Quantification, ISMRM 2024 conference abstract, Singapore.]
```
```