import argparse
import glob
import os
import time
from functools import partial

import nibabel as nib
import numpy as np
import torch
from nibabel import processing
from tqdm import tqdm as std_tqdm

from utils.hemisphere import hemisphere
from utils.parcellation import parcellation
from utils.postprocessing import postprocessing
from utils.preprocessing import preprocessing
from utils.stripping import stripping
from utils.make_csv import make_csv
from utils.load_model import load_model

tqdm = partial(std_tqdm, dynamic_ncols=True)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input folder")
    parser.add_argument("-o", help="output folder")
    parser.add_argument("-m", help="model path")
    return parser.parse_args()

def main():
    # print(
    #     "\n#######################################################################\n"
    #     "Please cite the following paper when using OpenMAP-T1:\n"
    #     "Kei Nishimaki, Kengo Onda, Kumpei Ikuta, Yuto Uchida, Hitoshi Iyatomi, Kenichi Oishi (2024).\n"
    #     "OpenMAP-T1: A Rapid Deep Learning Approach to Parcellate 280 Anatomical Regions to Cover the Whole Brain.\n"
    #     "paper: https://www.medrxiv.org/content/10.1101/2024.01.18.24301494v1.\n"
    #     "#######################################################################\n"
    #     )
    opt = create_parser()
    device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    cnet, ssnet, pnet_c, pnet_s, pnet_a, hnet_c, hnet_a = load_model(opt, device)

    print("load complete !!")
    pathes = sorted(glob.glob(os.path.join(opt.i, "**/*.nii"), recursive=True))

    for i, path in tqdm(enumerate(pathes)):
        save = os.path.basename(path)
        odata = nib.squeeze_image(nib.as_closest_canonical(nib.load(path)))
        nii = nib.Nifti1Image(odata.get_fdata().astype(np.float32), affine=odata.affine)

        if i % 5 == 0:
            dirname = save.replace("_00.nii", "")
            output_dir = f"{opt.o}/{dirname}"
            os.makedirs(output_dir, exist_ok=True)
            nib.save(nii, os.path.join(output_dir, f"{save}"))
            
            odata, data0 = preprocessing(path, save)
            os.remove(f"N4/{save}")
        
        elif i % 5 == 1:
            nib.save(nii, os.path.join(output_dir, f"{save}"))
            
            odata, data1 = preprocessing(path, save)
            out_e = stripping(data0, data1, ssnet, device)
            os.remove(f"N4/{save}")
        
        elif i % 5 == 2:
            nib.save(nii, os.path.join(output_dir, f"{save}"))
            data2 = processing.conform(odata, out_shape=(256, 256, 256), voxel_size=(0.6, 0.6, 0.6), order=1)
        
        elif i % 5 == 3:
            nib.save(nii, os.path.join(output_dir, f"{save}"))
            data3 = processing.conform(odata, out_shape=(256, 256, 256), voxel_size=(0.6, 0.6, 0.6), order=1)
        
        else:
            nib.save(nii, os.path.join(output_dir, f"{save}"))
            data4 = processing.conform(odata, out_shape=(256, 256, 256), voxel_size=(0.6, 0.6, 0.6), order=1)    
            
            parcellated = parcellation(data0, data1, data2, data3, data4, pnet_c, pnet_s, pnet_a, device)
            separated = hemisphere(data0, data1, hnet_c, hnet_a, device)
            output = postprocessing(parcellated, separated)

            df = make_csv(output, dirname)
            df.to_csv(os.path.join(output_dir, f"{dirname}_volume.csv"), index=False)

            nii = nib.Nifti1Image(output.astype(np.uint16), affine=data4.affine)
            header = odata.header
            nii = processing.conform(nii, out_shape=(header["dim"][1], header["dim"][2], header["dim"][3]), voxel_size=(header["pixdim"][1], header["pixdim"][2], header["pixdim"][3]), order=0)
            nib.save(nii, os.path.join(output_dir, f"{dirname}_168.nii"))
    return

if __name__ == "__main__":
    main()
