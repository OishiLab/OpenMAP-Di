import torch
from scipy.ndimage import binary_dilation
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
    
def hemisphere(out_e, data0, data1, hnet_c, hnet_a, device):
    voxel0 = (data0.get_fdata() * out_e).astype(np.float32)
    voxel0 = normalize_dwib0(voxel0)[np.newaxis]
    voxel1 = (data1.get_fdata() * out_e).astype(np.float32)
    voxel1 = normalize_dwib0(voxel1)[np.newaxis]
    
    voxel = np.concatenate([voxel0, voxel1], axis=0)
    
    coronal = voxel.transpose(1, 2, 0)
    axial = voxel.transpose(2, 1, 0)
    out_c = separate(coronal, hnet_c, device).permute(1, 3, 0, 2)
    out_a = separate(axial, hnet_a, device).permute(1, 3, 2, 0)
    out_e = out_c + out_a * 2
    del out_c, out_a
    out_e = torch.argmax(out_e, 0).cpu().numpy()
    torch.cuda.empty_cache()
    
    dilated_mask_1 = binary_dilation(out_e == 1, iterations=10).astype("int16")
    dilated_mask_1[out_e == 2] = 2
    dilated_mask_1[out_e == 3] = 3
    dilated_mask_1[out_e == 4] = 4
    dilated_mask_2 = binary_dilation(dilated_mask_1 == 2, iterations=10).astype("int16")*2
    dilated_mask_2[dilated_mask_1 == 1] = 1
    dilated_mask_2[dilated_mask_1 == 3] = 3
    dilated_mask_2[dilated_mask_1 == 4] = 4
    return dilated_mask_2
