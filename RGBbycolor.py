import glob
import nibabel as nib
import numpy as np
import shutil
import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input color folder")
    parser.add_argument("-o", help="output folder")
    return parser.parse_args()

def main():
    opt = create_parser()
    pathes = sorted(glob.glob(os.path.join(opt.i, "**/*.nii"), recursive=True))
    
    for path in tqdm(pathes):
        for i in range(3):
            name1 = os.path.basename(path).replace(".nii","")
            name = name1 + f"_0{i+2}.nii"
            output_dir = f"{opt.o}/{name}"
            
            data1 = nib.squeeze_image(nib.as_closest_canonical(nib.load(path)))
            dtype = data1.get_data_dtype()
            scan = np.asanyarray(data1.dataobj)
            scan = scan.copy().view(scan.dtype[0]).reshape(scan.shape + (-1,))
            scan_RGB = scan[:, :, :, i]
            voxel_RGB = scan_RGB.astype("float32")
            data2 = nib.Nifti1Image(voxel_RGB.astype(np.float32), affine=data1.affine)
            nib.save(data2, f'{output_dir}')

if __name__ == "__main__":
    main()
