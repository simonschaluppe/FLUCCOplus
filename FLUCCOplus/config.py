from pathlib import Path

# imports shared throughout the project
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


import sys
import importlib


from FLUCCOplus.utils import logg, PJ_TO_GWH, GWH_TO_PJ, log



DATA_RAW = Path("../data/raw")
DATA_EXTERNAL = Path("../data/external")
DATA_INTERIM = Path("../data/interim")
DATA_PROCESSED = Path("../data/processed")



VERBOSE = True


if VERBOSE:
    print(__name__, " loaded!")