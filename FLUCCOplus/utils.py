

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


def plot_signal_bars(df, columns, ytick_average_max=False):
    """takes a df series, with -1 and +1 denoting OFF and ON signals"""
    desc_wind = pd.DataFrame()
    df_step_wind = pd.DataFrame()
    df_not_wind = pd.DataFrame()

    # fig, ax = plt.subplots()
    for c in columns:
        df_step_wind[c] = df[c].shift(1).ne(df[c]).where(df[c] == 1).cumsum()
        df_not_wind[c] = df[c].shift(1).ne(df[c]).where(df[c] == -1).cumsum()
    df_step_wind.iloc[0, :] = 0
    desc_wind["Zeitraum mit Signal [h]"] = df.where(df > 0).sum()
    desc_wind["Nicht-Signal-Zeitraum [h]"] = 8760 - desc_wind["Zeitraum mit Signal [h]"]
    desc_wind["Anzahl Signal-Perioden"] = df_step_wind.max()
    desc_wind["Durchschnittliche Dauer Signal [h]"] = (
                desc_wind["Zeitraum mit Signal [h]"] / desc_wind["Anzahl Signal-Perioden"])
    desc_wind["Durchschnittliche Dauer Nicht-Signal [h]"] = desc_wind["Nicht-Signal-Zeitraum [h]"] / desc_wind[
        "Anzahl Signal-Perioden"]

    fig, ax = plt.subplots(1, 2, figsize=(12, 7))
    desc_wind.loc[columns][["Zeitraum mit Signal [h]", "Nicht-Signal-Zeitraum [h]"]] \
        .plot(kind="bar", color=["cyan", "black"], stacked=True, ax=ax[0]).set(ylabel="Stunden")
    desc_wind.loc[columns][["Durchschnittliche Dauer Signal [h]", "Durchschnittliche Dauer Nicht-Signal [h]"]] \
        .plot(kind="bar", color=["orange", "grey"], stacked=False, ax=ax[1]).set(ylabel="Stunden")
    for p in ax[0].patches:
        ax[0].annotate("{:.1f}%".format(p.get_height() * 100 / 8760),
                       (p.get_x() + p.get_width() / 2., p.get_height() + p.get_y() - 5), ha='center', va='center',
                       fontsize=7, color='black', xytext=(0, -8), textcoords='offset points')
    for p in ax[1].patches:
        ax[1].annotate("{:.0f}".format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                       va='center', fontsize=7, color='black', xytext=(0, -8), textcoords='offset points')
    if ytick_average_max:
        ax[1].yaxis.set_ticks(np.arange(0, ytick_average_max, 24))  # TODO: as function parameters
    plt.grid(axis="x")
    return fig, ax


if __name__ == "__main__":
    @log
    def test():
        pass

    test()


