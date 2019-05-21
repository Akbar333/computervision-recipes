# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from pathlib import PosixPath
import random
import shutil
from typing import List, Union 

import numpy as np


def set_random_seed(s: int):
    """Set random seed
    """
    np.random.seed(s)
    random.seed(s)

    try:
        import torch

        torch.manual_seed(s)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(s)
            torch.cuda.manual_seed_all(s)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    
def copy_files(fpaths: Union[str, List[str]], dst: str, infer_subdir: bool = False, remove: bool = False):
    """Copy list of files into destination
    
    Args:
        fpaths: File path to copy
        dst: Destination directory
        infer_subdir: If True, try to infer directory structure of the files and copy.
            Otherwise, just copy the files to dst
        remove: Remove copied files from the original directory
    """
    if isinstance(fpaths, (str, PosixPath)):
        fpaths = [fpaths]
    
    for fpath in fpaths:
        if infer_subdir:
            dst = os.path.join(dst, os.path.basename(os.path.dirname(fpath)))
            
        if not os.path.isdir(dst):
            os.makedirs(dst)
        shutil.copy(fpath, dst)
        
        if remove:
            os.remove(fpath)