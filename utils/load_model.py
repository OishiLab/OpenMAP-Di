import os
import torch
from utils.network import UNet

def load_model(opt, device):
    ssnet = UNet(2, 1)
    ssnet.load_state_dict(torch.load(os.path.join(opt.m, "SSNet/SSNet.pth")))
    ssnet.to(device)
    ssnet.eval()

    pnet_c = UNet(5, 86)
    pnet_c.load_state_dict(torch.load(os.path.join(opt.m, "PNet/coronal.pth")))
    pnet_c.to(device)
    pnet_c.eval()

    pnet_s = UNet(5, 86)
    pnet_s.load_state_dict(torch.load(os.path.join(opt.m, "PNet/sagittal.pth")))
    pnet_s.to(device)
    pnet_s.eval()

    pnet_a = UNet(5, 86)
    pnet_a.load_state_dict(torch.load(os.path.join(opt.m, "PNet/axial.pth")))
    pnet_a.to(device)
    pnet_a.eval()

    hnet_c = UNet(2, 5)
    hnet_c.load_state_dict(torch.load(os.path.join(opt.m, "HNet/coronal.pth")))
    hnet_c.to(device)
    hnet_c.eval()

    hnet_a = UNet(2, 5)
    hnet_a.load_state_dict(torch.load(os.path.join(opt.m, "HNet/axial.pth")))
    hnet_a.to(device)
    hnet_a.eval()
    return ssnet, pnet_c, pnet_s, pnet_a, hnet_c, hnet_a