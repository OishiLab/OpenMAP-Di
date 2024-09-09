import numpy as np
import torch
from scipy import ndimage
from utils.functions import normalize


def strip(voxel, model, device):
    model.eval()
    with torch.inference_mode():
        output = torch.zeros(256, 256, 256).to(device)
        for i in range(256):
            image = voxel[:, i, :, :].reshape(1, 2, 256, 256)
            image = torch.tensor(image).to(device)
            x_out = torch.sigmoid(model(image)).detach()
            if i == 0:
                output[0] = x_out
            else:
                output[i] = x_out
        return output.reshape(256, 256, 256)
    
def stripping(data0, data1, ssnet, device):
    voxel0 = data0.get_fdata()
    voxel0 = normalize(voxel0)[np.newaxis]
    voxel1 = data1.get_fdata()
    voxel1 = normalize(voxel1)[np.newaxis]
    
    voxel = np.concatenate([voxel0, voxel1], axis=0)
    
    coronal = voxel.transpose(0, 2, 3, 1)
    sagittal = voxel
    axial = voxel.transpose(0, 3, 2, 1)
    out_c = strip(coronal, ssnet, device).permute(2,0,1)
    out_s = strip(sagittal, ssnet, device)
    out_a = strip(axial, ssnet, device).permute(2,1,0)
    out_e = ((out_c + out_s + out_a * 2) / 4) > 0.5
    out_e = out_e.cpu().numpy()
    return stripped
