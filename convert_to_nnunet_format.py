from pathlib import Path
import nibabel
import numpy as np

import argparse


def convert_scan(in_file: Path, out_file: Path) -> int:
    """
    Converts ANALYZE .img/.hdr file into NIfTI .nii.gz file format

    :param in_file: path to ANALYZE .img input file
    :param out_file: path to NIfTI .nii.gz output file
    :return: number of files outputted
    """

    data = nibabel.funcs.squeeze_image(nibabel.load(in_file))
    dtype = data.get_data_dtype()
    scan = np.asanyarray(data.dataobj)
    if dtype == [('R', 'u1'), ('G', 'u1'), ('B', 'u1')]:  # color scan
        scan = scan.copy().view(scan.dtype[0]).reshape(scan.shape + (-1,))
        idx_str = out_file.name.replace(''.join(out_file.suffixes), '').split('_')[-1]
        for channel in range(scan.shape[3]):
            nibabel.save(nibabel.Nifti1Image(scan[:, :, :, channel], data.affine),
                         str(out_file).replace(idx_str, "{:04d}".format(int(idx_str)+channel)))
        return scan.shape[3]
    else:
        nibabel.save(nibabel.Nifti1Image(scan.astype(dtype), data.affine), out_file)
        return 1


def convert_to_nnunet_format(nnunet_folder: Path, dwi_file: Path, b0_file: Path, color_file: Path, subject: str) -> None:
    """
    Converts dwi, b0, and color ANALYZE .img/.hdr scans into the nnU-Net data format

    :param nnunet_folder: path to nnU-Net input folder
    :param dwi_file: path to dwi ANALYZE .img file
    :param b0_file: path to dwi ANALYZE .img file
    :param color_file: path to dwi ANALYZE .img file
    :param subject: subject identifier
    """
    nnunet_folder.mkdir(exist_ok=True)
    files = [dwi_file, b0_file, color_file]
    idx = 0
    for file in files:
        num_output = convert_scan(file, nnunet_folder / (subject + "_{:04d}".format(idx) + ".nii.gz"))
        idx += num_output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use this to convert dwi, b0, and color ANALYZE scans into the '
                                                 'nnU-Net data format.')
    parser.add_argument('-i', type=str, required=True,
                        help='The nnU-Net input folder. If it does not exist it will be created.')
    parser.add_argument('-d', type=str, required=True,
                        help='The dwi .img file.')
    parser.add_argument('-b', type=str, required=True,
                        help='The b0 .img file.')
    parser.add_argument('-c', type=str, required=True,
                        help='The color .img file.')
    parser.add_argument('-s', type=str, required=True,
                        help='The subject identifier.')
    args = parser.parse_args()
    convert_to_nnunet_format(Path(args.i), Path(args.d), Path(args.b), Path(args.c), args.s)
