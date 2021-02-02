

# imports shared throughout the project
import sys
import importlib

import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# CONSTANTS

PJ_TO_GWH = 277.7778 # [GWh / PJ]
GWH_TO_PJ = 1/PJ_TO_GWH #[PJ/GWH]


# HELPER
import FLUCCOplus.config as config

def log(f):
    logger = config.logging.getLogger(f.__module__)
    def wrapper(*args, **kwargs):
        tic = time.time()*1000
        result = f(*args, **kwargs)
        toc = time.time()*1000
        logger.info(f"{f.__name__} - {round(toc-tic,2)}ms")
        return result
    return wrapper

def logg(f):
    logger = config.logging.getLogger(f.__module__)

    def wrapper(dataframe, *args, **kwargs):

        result = log(f)(dataframe, *args, **kwargs)
        ro, co = result.shape
        logger.debug(f"{f.__name__} df.shape = ({ro}, {co})")

        return result
    return wrapper


if __name__ == "__main__":
    @log
    def test():
        pass

    test()