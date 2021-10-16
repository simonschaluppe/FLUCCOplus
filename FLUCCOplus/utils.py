

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

EM_TO_EXCEL_colnames = {
    "power_production_wind_avg": "Windkraft",
    "power_production_solar_avg": "Photovoltaik",
    "power_production_hydro_avg": "Laufkraft",
    "total_consumption_avg": "Strombedarf",
    "total_production_avg": "Stromproduktion",
    "power_consumption_hydro_discharge_avg": "Pumpspeicher"}

EXCEL_TO_EM_colnames = {v: k for k, v in EM_TO_EXCEL_colnames.items()}
EXCEL_TO_EM_colnames["Volatile EE"] = "power_production_volatile_avg"
EXCEL_TO_EM_colnames["Nicht-Volatile"] = "power_production_non-volatile_avg"
EXCEL_TO_EM_colnames["Pumpspeicher"] = "power_consumption_hydro_discharge_avg"
EXCEL_TO_EM_colnames["Wasserkraft"] = "power_production_hydro_and_discharge_avg"





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