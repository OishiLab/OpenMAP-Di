import numpy as np
import torch
from scipy.ndimage import binary_dilation, label, find_objects
from utils.functions import normalize_dwib0


def separate(voxel, model, device):
    model.eval()
    voxel = np.pad(voxel, [(0,0), (1, 1), (0, 0), (0, 0)], "constant", constant_values=voxel.min())
    with torch.inference_mode():
        box = torch.zeros(256, 5, 256, 256)
        for i in range(256):
            i += 1
            image = voxel[:,i,:,:]
            image = torch.tensor(image.reshape(1, 2, 256, 256),dtype=torch.float32)
            image = image.to(device)
            box[i - 1] = torch.softmax(model(image),1)
        return box

def remove_small_areas(brain_map, target_label):
    mask = brain_map == target_label
    labeled_array, num_features = label(mask)
    sizes = np.bincount(labeled_array.ravel())
    sizes[0] = 0
    largest_region = sizes.argmax()

    for i in range(1, num_features + 1):
        if i != largest_region:
            region_mask = labeled_array == i
            brain_map[region_mask] = get_surrounding_label(brain_map, region_mask)
    return brain_map

def get_surrounding_label(brain_map, region_mask):
    expanded_mask = np.pad(region_mask, 1, mode='constant', constant_values=0)
    surrounding_labels = brain_map[expanded_mask[1:-1, 1:-1, 1:-1] == 0]
    surrounding_labels = surrounding_labels[surrounding_labels > 0]

    if len(surrounding_labels) == 0:
        return 0 

    return np.bincount(surrounding_labels).argmax()
    
def hemisphere(out_e, data0, data1, hnet_c, hnet_a, device):
    voxel0 = (data0.get_fdata() * out_e).astype(np.float32)
    voxel0 = normalize_dwib0(voxel0)[np.newaxis]
    voxel1 = (data1.get_fdata() * out_e).astype(np.float32)
    voxel1 = normalize_dwib0(voxel1)[np.newaxis]
    
    voxel = np.concatenate([voxel0, voxel1], axis=0)
    
    coronal = voxel.transpose(0, 2 ,3, 1)
    axial = voxel.transpose(0, 3, 2, 1)
    out_c = separate(coronal, hnet_c, device).permute(1, 3, 0, 2)
    out_a = separate(axial, hnet_a, device).permute(1, 3, 2, 0)
    out_e = out_c + out_a * 2
    del out_c, out_a
    out_e = torch.argmax(out_e, 0).cpu().numpy()
    out_e = remove_small_areas(out_e, target_label=1)
    out_e = remove_small_areas(out_e, target_label=2)
    
    dilated_mask_1 = binary_dilation(out_e == 1, iterations=10).astype("int16")
    dilated_mask_1[out_e == 2] = 2
    dilated_mask_1[out_e == 3] = 3
    dilated_mask_1[out_e == 4] = 4
    dilated_mask_2 = binary_dilation(dilated_mask_1 == 2, iterations=10).astype("int16")*2
    dilated_mask_2[dilated_mask_1 == 1] = 1
    dilated_mask_2[dilated_mask_1 == 3] = 3
    dilated_mask_2[dilated_mask_1 == 4] = 4
    torch.cuda.empty_cache()
    return dilated_mask_2
