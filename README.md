![OpenMAP_Logo_with_name](https://github.com/OishiLab/OpenMAP-T1/assets/64403395/9ce68146-eeb7-4ce0-bd49-73f1c7ded4d8)

# OpenMAP-Di
**OpenMAP-Di parcellates an infant's DTI brain scan into 169 anatomical regions.**

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

3. Download the pre-trained model using this link (TBD).

4. Convert the data you would like to parcellate into the [nnU-Net dataset format](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_format.md). Channel numbers are defined in the `dataset.json` file within the pre-trained model folder.

6. Run `parcellate_neonatal_brain.py` to parcellate your dataset! See help (`-h`) for more details. Inferred parcellations will be outputted to the `OUTPUT_FOLDER`, while postprocessed parcellations will be outputted to a `postprocessing` subfolder of the `OUTPUT_FOLDER`.
```
python parcellate_neonatal_brain.py -i INPUT_FOLDER -o OUTPUT_FOLDER -m MODEL_FOLDER
```

## Citation
Coming soon!
```
```