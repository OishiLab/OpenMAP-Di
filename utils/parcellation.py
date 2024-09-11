import numpy as np
import torch
from utils.functions import normalize
from utils.functions import normalize_dwib0


def parcellate(voxel, model, device):
    model.eval()
    voxel = np.pad(voxel, [(0, 0), (1, 1), (0, 0), (0, 0)], "constant", constant_values=voxel.min())
    with torch.inference_mode():
        box = torch.zeros(256, 86, 256, 256)
        for i in range(256):
            i += 1
            image = voxel[:,i,:,:]
            image = torch.tensor(image.reshape(1, 5, 256, 256),dtype=torch.float32)
            image = image.to(device)
            box[i - 1] = torch.softmax(model(image),1).detach().cpu()
        return box
    
def parcellation(out_e, data0, data1, data2, data3, data4, pnet_c, pnet_s, pnet_a, device):
    voxel0 = (data0.get_fdata() * out_e).astype(np.float32)
    voxel0 = normalize_dwib0(voxel0)[np.newaxis]
    voxel1 = (data1.get_fdata() * out_e).astype(np.float32)
    voxel1 = normalize_dwib0(voxel1)[np.newaxis]
    voxel2 = (data2.get_fdata() * out_e).astype(np.float32)
    voxel2 = normalize(voxel2)[np.newaxis]
    voxel3 = (data3.get_fdata() * out_e).astype(np.float32)
    voxel3 = normalize(voxel3)[np.newaxis]
    voxel4 = (data4.get_fdata() * out_e).astype(np.float32)
    voxel4 = normalize(voxel4)[np.newaxis]
    
    voxel = np.concatenate([voxel0, voxel1, voxel2, voxel3, voxel4], axis=0)
    
    coronal = voxel.transpose(0, 2, 3, 1)
    axial = voxel.transpose(0, 3, 2, 1)
    sagittal = voxel
    
    out_c = parcellate(coronal, pnet_c, device).permute(1, 3, 0, 2)
    torch.cuda.empty_cache()
    out_s = parcellate(sagittal, pnet_s, device).permute(1, 0, 2, 3)
    torch.cuda.empty_cache()
    out_e = out_c + out_s
    del out_c, out_s
    out_a = parcellate(axial, pnet_a, device).permute(1, 3, 2, 0)
    torch.cuda.empty_cache()
    out_e = out_e + out_a * 2
    del out_a
    parcellated = torch.argmax(out_e, 0).numpy()
    return parcellated
