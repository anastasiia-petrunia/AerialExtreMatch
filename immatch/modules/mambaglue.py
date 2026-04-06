import numpy as np
import torch
import sys
from pathlib import Path

from .base import Matching
from immatch.utils.data_io import load_im_tensor


# Use if statement to prevent formatting from corrupting the code
if True:
    import sys
    from pathlib import Path
    mamba_path = "/content"
    sys.path.append(str(mamba_path))
    from mambaglue.mambaglue import MambaGlue as _MambaGlue
    from mambaglue.superpoint import SuperPoint


class MambaGlue(Matching):
    def __init__(self, args):
        super().__init__()
        
        # Load parameters from the config file
        self.imsize = args.get("imsize", -1)
        self.max_num_keypoints = args.get("num_keypoints", 4096)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize Extractor (SuperPoint) and Matcher (MambaGlue)
        self.extractor = SuperPoint(max_num_keypoints=self.max_num_keypoints).eval().to(self.device)
        self.matcher = _MambaGlue(features='superpoint', filter_threshold=0.0).eval().to(self.device)

        self.name = "MambaGlue"
        print(f"Initialize {self.name}")

    def load_im(self, im_path):
        # Use the built-in flags to get exactly what SuperPoint needs
        rgb_tensor, gray_tensor, scale = load_im_tensor(
            im_path,
            device=self.device,
            imsize=self.imsize,
            normalize=False,  # Stops the negative ImageNet scaling
            with_gray=True    # Generates the [1, 1, H, W] Grayscale tensor
        )
        
        # We only need the grayscale tensor and the scale for SuperPoint
        return gray_tensor, scale

    def match_pairs(self, im1_path, im2_path):
        # 1. Load images and get scale factors
        im1, sc1 = self.load_im(im1_path)
        im2, sc2 = self.load_im(im2_path)
        upscale = np.array([sc1 + sc2]) # [scale_x1, scale_y1, scale_x2, scale_y2]

        # 2. Extract and Match
        with torch.no_grad():
            pred1 = self.extractor({'image': im1})
            pred2 = self.extractor({'image': im2})
            
            data = {
                'image0': {k: v for k, v in pred1.items()},
                'image1': {k: v for k, v in pred2.items()}
            }
            
            pred = self.matcher(data)
            
        # 3. Parse output matches
        matches0 = pred['matches0'][0].cpu().numpy()
        valid = matches0 > -1
        
        mkpts1 = pred1['keypoints'][0].cpu().numpy()[valid]
        mkpts2 = pred2['keypoints'][0].cpu().numpy()[matches0[valid]]
        
        # Concatenate into Nx4 array
        matches = np.concatenate([mkpts1, mkpts2], axis=1)
        
        # 4. Scale keypoints back to original image resolutions
        matches = upscale * matches

        # The benchmark expects 4 outputs, we return Nones for the unused ones
        return matches, None, None, None