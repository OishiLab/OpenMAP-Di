# OpenMAP-T1-V1
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fmfkxxZjChExnl5cHITYkNYgTu3MZ7Ql#scrollTo=xwZxyL5ewVNF)

**OpenMAP-T1-V1 parcellates the whole brain into 280 anatomical regions based on JHU-atlas in 90 (sec/case).**

We are publishing demonstration.

## Installation Instructions
0. install python and make virtual environment<br>
python3.8 or later is recommended.

1. Clone this repository:
```
git clone https://github.com/OishiLab/OpenMAP-T1-V1.git
```
2. Please install PyTorch compatible with your environment.<br>
https://pytorch.org/

Once you select your environment, the required commands will be displayed.

<img width="485" alt="image" src="https://github.com/OishiLab/OpenMAP-T1-V1/assets/64403395/eb092ff6-6597-4237-ac3a-aa0695bff631">

If you want to install an older Pytorch environment, you can download it from the link below.<br>
https://pytorch.org/get-started/previous-versions/

4. Go into the repository and install:
```
cd OpenMAP-T1-V1
pip install -r requirements.txt
```

## How to use it
Using OpenMAP-T1 is straightforward. You can use it in any terminal on your linux system. The OpenMAP-T1 command was installed automatically. We provide CPU as well as GPU support. Running on GPU is a lot faster though and should always be preferred. Here is a minimalistic example of how you can use OpenMAP-T1.
```
python3 parcellation.py -i INPUR_DIRNAME -o OUTPUT_DIRNAME -m MODEL_DIRNAME
```
If you want to specify the GPU, please add ```--gpu```.
```
python3 parcellation.py -i INPUR_DIRNAME -o OUTPUT_DIRNAME -m MODEL_DIRNAME --gpu 1
```

### Folder
```
INPUR_DIRNAME/
  ├ A.nii
  ├ B.nii
  ├ *.nii

OUTPUT_DIRNAME/
  ├ input/
  |   ├ A.nii
  |   ├ B.nii
  |   ├ *.nii
  └ output/
      ├ A.nii
      ├ B.nii
      ├ *.nii

MODEL_DIRNAME/
  ├ CNet/CNet.pth
  ├ SSNet/SSNet.pth
  ├ PNet
  |   ├ coronal.pth
  |   ├ sagittal.pth
  |   └ axial.pth
  └ HNet/
      ├ coronal.pth
      └ axial.pth
```

## How to download the pretrained model.
You can get the pretrained model from the this link.
[Link of pretrained model](https://livejohnshopkins-my.sharepoint.com/:f:/g/personal/knishim4_jh_edu/EnMzAgDEcHpMqzmHw_vWOskBr6Ax2KQEMZFq8yG7KitkBQ?email=yuchida2%40jhmi.edu&e=bXE4pW)

## FAQ
* **How much GPU memory do I need to run HD-BET?** <br>
We ran all our experiments on NVIDIA RTX3090 GPUs with 24 GB memory. For inference you will need less, but since inference in implemented by exploiting the fully convolutional nature of CNNs the amount of memory required depends on your image. Typical image should run with less than 4 GB of GPU memory consumption. If you run into out of memory problems please check the following: 1) Make sure the voxel spacing of your data is correct and 2) Ensure your MRI image only contains the head region.

* **Will you provide the training code as well?** <br>
No. The training code is tightly wound around the data which we cannot make public.

## Citation
```
@article{nishimaki2024openmap-t1,
  title={OpenMAP-T1: A Rapid Deep-Learning Approach to Parcellate 280 Anatomical Regions to Cover the Whole Brain},
  author={Kei Nishimaki, Kengo Onda, Kumpei Ikuta, Jill Chotiyanonta, Yuto Uchida, Susumu Mori, Hitoshi Iyatomi, Kenichi Oishi},
  journal={~~~~},
  year={2024},
  publisher={~~~~}
}
```
