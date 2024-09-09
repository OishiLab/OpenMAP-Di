![OpenMAP_Logo_with_name](https://github.com/OishiLab/OpenMAP-T1/assets/64403395/9ce68146-eeb7-4ce0-bd49-73f1c7ded4d8)

# OpenMAP-Di-V2
**OpenMAP-Di parcellates the whole brain into 168 anatomical regions based on JHU-atlas in 60 (sec/case).**

## Installation Instructions
0. install python and make virtual environment<br>
python3.8 or later is recommended.

1. Clone this repository:
```
git clone -b v2.0.0 https://github.com/OishiLab/OpenMAP-Di-V2.git
```
2. Please install PyTorch compatible with your environment.<br>
https://pytorch.org/

Once you select your environment, the required commands will be displayed.

![image](https://github.com/OishiLab/OpenMAP-T1/v2.0.0/media/PyTorch.png)

If you want to install an older Pytorch environment, you can download it from the link below.<br>
https://pytorch.org/get-started/previous-versions/

4. Go into the repository and install:
```
cd OpenMAP-Di-V2
pip install -r requirements.txt
```

## How to use it
Using OpenMAP-Di is straightforward. You can use it in any terminal on your linux system. We provide CPU as well as GPU support. Running on GPU is a lot faster though and should always be preferred. Here is a minimalistic example of how you can use OpenMAP-Di.
```
python3 parcellation.py -i INPUT_DIRNAME -o OUTPUT_DIRNAME -m MODEL_DIRNAME
```
If you want to specify the GPU, please add ```CUDA_VISIBLE_DEVICES=N```.
```
CUDA_VISIBLE_DEVICES=1 python3 parcellation.py -i INPUT_DIRNAME -o OUTPUT_DIRNAME -m MODEL_DIRNAME
```

## How to download the pretrained model.
You can get the pretrained model from the this link.
[Link of pretrained model](https://forms.office.com/Pages/ResponsePage.aspx?id=OPSkn-axO0eAP4b4rt8N7Iz6VabmlEBIhG4j3FiMk75UNkxFRk5IRkY3MjJaNU9POUZBNlNQRzUxVy4u)

## Folder
All images you input must be in NifTi format and have a .nii extension.
```
INPUT_DIRNAME/
  ├ A_00.nii(DWI)
  ├ A_01.nii(B0)
  ├ A_02.nii(COLOR_R)
  ├ A_03.nii(COLOR_G)
  ├ A_04.nii(COLOR_B)
  ├ B_00.nii(DWI)
  ├ B_01.nii(B0)
  ├ B_02.nii(COLOR_R)
  ├ B_03.nii(COLOR_G)
  ├ B_04.nii(COLOR_B)
  ├ ...

OUTPUT_DIRNAME/
  ├ A/
  |   ├ A.nii # input image
  |   ├ A_volume.csv # volume information (mm^3)
  |   └ A_168.nii # parcellation map
  └ B/
      ├ B.nii
      ├ B_volume.csv
      └ B_168.nii
  |
  └ ...

MODEL_DIRNAME/
  ├ SSNet/SSNet.pth
  ├ PNet
  |   ├ coronal.pth
  |   ├ sagittal.pth
  |   └ axial.pth
  └ HNet/
      ├ coronal.pth
      └ axial.pth
```

## FAQ
* **How much GPU memory do I need to run OpenMAP-Di?** <br>
We ran all our experiments on NVIDIA TITAN RTX GPUs with 24 GB memory. For inference you will need less, but since inference in implemented by exploiting the fully convolutional nature of CNNs the amount of memory required depends on your image. Typical image should run with less than 4 GB of GPU memory consumption. If you run into out of memory problems please check the following: 1) Make sure the voxel spacing of your data is correct and 2) Ensure your MRI image only contains the head region.

* **Will you provide the training code as well?** <br>
No. The training code is tightly wound around the data which we cannot make public.
