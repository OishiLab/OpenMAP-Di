import sys
from nnunetv2.inference.predict_from_raw_data import predict_entry_point_modelfolder
from nnunetv2.postprocessing.remove_connected_components import entry_point_apply_postprocessing
from pathlib import Path

import argparse


def parcellate_neonatal_brain(model_folder, input_folder, output_folder, device):
    # Run inference
    sys.argv = [sys.argv[0],
                '-m', model_folder,
                '-i', input_folder,
                '-o', output_folder,
                '-device', device,
                '-npp', '1',
                '-nps', '1']
    predict_entry_point_modelfolder()

    # Run post-processing
    sys.argv = [sys.argv[0],
                '-i', output_folder,
                '-o', str(Path(output_folder) / 'postprocessing'),
                '-pp_pkl_file', str(Path(model_folder) / 'crossval_results_folds_0_1_2_3_4' / 'postprocessing.pkl')]
    entry_point_apply_postprocessing()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use this to run inference and post-process with nnU-Net.')
    parser.add_argument('-i', type=str, required=True,
                        help='Input folder. Remember to use the correct channel numberings for your files (_0000 etc) '
                             'and match the channel numbers to the channel_names recorded in dataset.json '
                             'within the model folder.')
    parser.add_argument('-o', type=str, required=True,
                        help='Output folder. If it does not exist it will be created. Predicted segmentations will '
                             'have the same name as their source images.')
    parser.add_argument('-m', type=str, required=True,
                        help='Folder in which the trained model is. Must have subfolders fold_X for the different '
                             'folds you trained.')
    parser.add_argument('-device', type=str, default='cuda', required=False,
                        help="Use this to set the device the inference should run with. Available options are 'cuda' "
                             "(GPU), 'cpu' (CPU) and 'mps' (Apple M1/M2). Do NOT use this to set which GPU ID! "
                             "Use CUDA_VISIBLE_DEVICES=X nnUNetv2_predict [...] instead!")
    args = parser.parse_args()
    parcellate_neonatal_brain(args.m, args.i, args.o, args.device)
