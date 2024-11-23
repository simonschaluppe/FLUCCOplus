

# imports shared throughout the project
import sys
import importlib

import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




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
    "total_production_avg": "Erzeugung",
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

def set_datetime_index(df, year=2018):
    dates = np.arange(f"{year}-01-01", f"{year+1}-01-01 00:00", dtype="datetime64[h]")
    df.index = dates
    return df

def plot_signal_bars(df, columns=None, ytick_average_max=False, cut_ylim=False, figsize=(12,6)):
    """takes a df series, with -1 and +1 denoting OFF and ON signals"""
    desc_wind = pd.DataFrame()
    df_step_wind = pd.DataFrame()
    df_not_wind = pd.DataFrame()
    
    columns = columns or df.columns

    # fig, ax = plt.subplots()
    for c in columns:
        df_step_wind[c] = df[c].shift(1).ne(df[c]).where(df[c] == 1).cumsum()
        df_not_wind[c] = df[c].shift(1).ne(df[c]).where(df[c] == -1).cumsum()
    df_step_wind.iloc[0, :] = 0
    desc_wind["Zeitraum mit Signal [h]"] = df.where(df > 0).sum()
    desc_wind["Nicht-Signal-Zeitraum [h]"] = len(df) - desc_wind["Zeitraum mit Signal [h]"]
    desc_wind["Anzahl Signal-Perioden"] = df_step_wind.max()
    desc_wind["Durchschnittliche Dauer Signal [h]"] = (
                    desc_wind["Zeitraum mit Signal [h]"] / desc_wind["Anzahl Signal-Perioden"])
    desc_wind["Durchschnittliche Dauer Nicht-Signal [h]"] = desc_wind["Nicht-Signal-Zeitraum [h]"] / desc_wind[
            "Anzahl Signal-Perioden"]

    fig, ax = plt.subplots(1, 2, figsize=figsize)
    desc_wind.loc[columns][["Zeitraum mit Signal [h]", "Nicht-Signal-Zeitraum [h]"]] \
        .plot(kind="bar", color=["cyan", "black"], stacked=True, ax=ax[0]).set(ylabel="Stunden")
    desc_wind.loc[columns][["Durchschnittliche Dauer Signal [h]", "Durchschnittliche Dauer Nicht-Signal [h]"]] \
        .plot(kind="bar", color=["orange", "grey"], stacked=False, ax=ax[1]).set(ylabel="Stunden")
    for p in ax[0].patches:
        ax[0].annotate("{:.1f}%".format(p.get_height() * 100 / len(df)),
                       (p.get_x() + p.get_width() / 2., p.get_height() + p.get_y() - 5), ha='center', va='center',
                       fontsize=7, color='black', xytext=(0, -8), textcoords='offset points')
    for p in ax[1].patches:
        ax[1].annotate("{:.0f}".format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                       va='center', fontsize=7, color='black', xytext=(0, -8), textcoords='offset points')
    if ytick_average_max:
        ax[1].yaxis.set_ticks(np.arange(0, ytick_average_max, 24))  # TODO: as function parameters
    if cut_ylim:
        plt.ylim(top=cut_ylim)
    plt.grid(axis="x")
    return fig, ax

def Ueberschuesse_PVfirst(df):
    df["Non_volatiles"] = df.Pumpspeicher + df.Laufkraft
    df["RESohneWind"] = df.Laufkraft + df.Photovoltaik + df.Pumpspeicher
    df["Residual_ohne_Wind"] = df.Strombedarf - df.Photovoltaik - df.Non_volatiles
    df["Zero"] = 0
    df["Wind_useful"] = (df[["Windkraft", "Residual_ohne_Wind"]]).min(axis=1).clip(0, None)
    df["WindkraftUeSch"] = 0  # Überschuss
    df["WindkraftDV"] = 0  # Direktverbrauch
    df["WindkraftLast"] = 0
    df["PVUeSch"] = 0  # Überschuss
    df["PVDV"] = 0 # Direktverbrauch
    for t in range(8760):
        if (df.Photovoltaik[t] + df.Non_volatiles[t]) >= df.Strombedarf[t]:
            df.WindkraftUeSch[t] = df.Windkraft[t]
            df.PVDV[t] = df.Strombedarf[t] - df.Non_volatiles[t]
            df.PVUeSch[t] = df.Photovoltaik[t] - df.PVDV[t]
        else:
            if df.RES[t] <= df.Strombedarf[t]:
                df.WindkraftUeSch[t] = 0
                df.PVUeSch[t] = 0
                df.WindkraftDV[t] = df.Windkraft[t]
                df.PVDV[t] = df.Photovoltaik[t]
            else:
                df.PVDV[t] = df.Photovoltaik[t]
                df.WindkraftDV[t] = df.Strombedarf[t] - (df.PVDV[t] + df.Non_volatiles[t])
                df.WindkraftUeSch[t] = df.Windkraft[t] - df.WindkraftDV[t]

        if df.RES[t] > df.Strombedarf[t]:
            df.WindkraftLast[t] = df.Strombedarf[t] - df.RES[t] + df.Windkraft[t]
    return df

def Ueberschuesse_WINDfirst(df2):
    df2["Non_volatiles"] = df2.Pumpspeicher + df2.Laufkraft
    df2["Zero"] = 0
    df2["Residual_ohne_Wind"] = df2.Strombedarf - df2.Non_volatiles
    df2["Wind_useful"] = (df2[["Windkraft", "Residual_ohne_Wind"]]).min(axis=1).clip(0, None)
    df2["WindkraftUeSch"] = 0  # Überschuss
    df2["WindkraftDV"] = 0
    df2["WindkraftLast"] = 0  # Direktverbrauch
    df2["PVUeSch"] = 0  # Überschuss
    df2["PVLast"] = 0  # Direktverbrauch
    df2["PVDV"] = 0
    for t in range(8760):
        if (df2.Windkraft[t] + df2.Non_volatiles[t]) <= df2.Strombedarf[t]:
            df2.WindkraftDV[t] = df2.Windkraft[t]
        if (df2.Windkraft[t] + df2.Non_volatiles[t]) > df2.Strombedarf[t]:
            if df2.Non_volatiles[t] > df2.Strombedarf[t]:
                df2.WindkraftUeSch[t] = df2.Windkraft[t]
            else:
                df2.WindkraftUeSch[t] = df2.Windkraft[t] + df2.Non_volatiles[t] - df2.Strombedarf[t]
                df2.WindkraftDV[t] = df2.Strombedarf[t] - df2.Non_volatiles[t]

        if (df2.Windkraft[t] + df2.Non_volatiles[t]) >= df2.Strombedarf[t]:
            df2.PVUeSch[t] = df2.Photovoltaik[t]
        elif (df2.Windkraft[t] + df2.Non_volatiles[t]) < df2.Strombedarf[t]:
            if df2.RES[t] < df2.Strombedarf[t]:
                df2.PVUeSch[t] = 0
                df2.PVDV[t] = df2.Photovoltaik[t]
            else:
                df2.PVDV[t] = df2.Strombedarf[t] - df2.Non_volatiles[t] - df2.WindkraftDV[t]
                df2.PVUeSch[t] = df2.Photovoltaik[t] - df2.PVDV[t]

    #    if df.RES[t] > df.Strombedarf[t]:
    #        df.PVLast[t] = df.Strombedarf[t] - df.RES[t] + df.Photovoltaik[t]
    #    if df.RES[t] > df.Strombedarf[t]:
    #       df.WindkraftLast[t] = df.Strombedarf[t] - df.RES[t] + df.Windkraft[t]
    df2["RESohnePV"] = df2.Laufkraft + df2.Windkraft + df2.Pumpspeicher
    df2["Residual_ohne_PV"] = df2.Strombedarf - df2.Photovoltaik - df2.Non_volatiles

    return df2

def maxnutz():
    from pathlib import Path
    output_file = config.DATA_PROCESSED / Path("MANutz/maxnutz_normalized.csv")
    
    # Check if the output file already exists
    if output_file.exists():
        # Load the existing file directly into a DataFrame and return it
        return pd.read_csv(output_file, sep=";", decimal=",")
    
    df_nutz["Schaltsignal_REF"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_REF.csv")).iloc[:, 1]
    df_nutz["Schaltsignal_REG"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_REG.csv")).iloc[:, 1]
    df_nutz["Schaltsignal_UBA30"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_uba30.csv")).iloc[:,
                                   1]
    df_nutz["Schaltsignal_UBA50"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_uba50.csv")).iloc[:,
                                   1]
    df_nutz["Schaltsignal_VEIGL30"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_veigl30.csv")).iloc[
                                     :, 1]
    df_nutz["Schaltsignal_VEIGL50"] = pd.read_csv(config.DATA_PROCESSED / Path("MANutz/Schaltsignal_veigl50.csv")).iloc[
                                     :, 1]
    df_nutz = df_nutz.replace(1, -1)
    df_nutz = df_nutz.replace(0, 1).replace(-1, 0)
    df_nutz.to_csv(output_file, sep=";", decimal=",")
    return df_nutz

if __name__ == "__main__":
    @log
    def test():
        pass

    test()


