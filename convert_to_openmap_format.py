from pathlib import Path
import nibabel as nib
import numpy as np

import argparse
import os
import glob

def convert_to_openmap_format(openmap_folder: Path, Input_folder: Path) -> None:
    dwi_pathes =  sorted(glob.glob(os.path.join(Input_folder, "**/*_dwi.nii"), recursive=True))
    b0_pathes =  sorted(glob.glob(os.path.join(Input_folder, "**/*_b0.nii"), recursive=True))
    color_pathes =  sorted(glob.glob(os.path.join(Input_folder, "**/*_color.nii"), recursive=True))

    os.makedirs(openmap_folder, exist_ok=True)
    for path in dwi_pathes:
        name = os.path.basename(path).replace("_dwi.nii","")
        data = nib.squeeze_image(nib.as_closest_canonical(nib.load(path)))
        nib.save(data, os.path.join(openmap_folder, f"{name}_00.nii"))

    for path in b0_pathes:
        name = os.path.basename(path).replace("_b0.nii","")
        data = nib.squeeze_image(nib.as_closest_canonical(nib.load(path)))
        nib.save(data, os.path.join(openmap_folder, f"{name}_01.nii"))

    for path in color_pathes:
        name = os.path.basename(path).replace("_color.nii","")
        data = nib.squeeze_image(nib.as_closest_canonical(nib.load(path)))
        
        for i in range(3):
            basename = name + f"_0{i+2}.nii"
            dtype = data.get_data_dtype()
            scan = np.asanyarray(data.dataobj)
            scan = scan.copy().view(scan.dtype[0]).reshape(scan.shape + (-1,))
            scan_RGB = scan[:, :, :, i]
            voxel_RGB = scan_RGB.astype("float32")
            nii = nib.Nifti1Image(voxel_RGB.astype(np.float32), affine=data.affine)
            nib.save(nii, os.path.join(openmap_folder, basename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use this to convert dwi, b0, and color scans into the '
    'OpenMAP data format.')
    parser.add_argument('-i', type=str, required=True,
    help='The OpenMAP input folder. If it does not exist it will be created.')
    parser.add_argument('-f', type=str, required=True,
    help='The folder to be converted.')
    args = parser.parse_args()
    convert_to_openmap_format(Path(args.i), Path(args.f))