import numpy as np

def ganma_corection(voxel, ganma):
    voxel = voxel / np.max(voxel)
    voxel = np.power(voxel, ganma)
    voxel = voxel * np.max(voxel)
    return voxel

def normalize(voxel):
    nonzero = voxel[voxel>0]
    voxel = np.clip(voxel, 0, np.mean(nonzero)+np.std(nonzero)*3)
    voxel = (voxel - np.mean(nonzero)) / np.std(nonzero)
    voxel = (voxel - np.min(voxel)) / (np.max(voxel) - np.min(voxel))
    voxel = (voxel * 2) - 1
    return voxel.astype("float32")

def normalize_dwib0(voxel):
    nonzero = voxel[voxel>0]
    voxel = np.clip(voxel, 0, np.mean(nonzero)+np.std(nonzero)*3)
    voxel = ganma_corection(voxel, 2)
    voxel = (voxel - np.mean(nonzero)) / np.std(nonzero)
    voxel = (voxel - np.min(voxel)) / (np.max(voxel) - np.min(voxel))
    voxel = (voxel * 2) - 1
    return voxel.astype("float32")