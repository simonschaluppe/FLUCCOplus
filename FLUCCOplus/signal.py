import pandas as pd

import  FLUCCOplus.utils as utils
import FLUCCOplus.config as config
import FLUCCOplus.web as web
import FLUCCOplus.transform as traffo
from pathlib import Path

PEEXCEL_PATH = config.DATA_PROCESSED / Path("peexcel_normalized.csv")
WEB_PATH = config.DATA_PROCESSED / Path("WEB_normalized.csv")
SPOT_PATH = config.DATA_PROCESSED / Path("DrexelCO2/Signale_CO2mix_SpotMarket.xlsx")
MANUTZ_PATH = config.DATA_PROCESSED / Path("MANutz/maxnutz_normalized.csv")

def load_peexcel():
    return pd.read_csv(PEEXCEL_PATH, index_col=0, parse_dates=True)


def load_web(year=None):
    df = web.read(WEB_PATH, decimal=",")
    if year:
        df = df[df.index.year==year]
    return df


def load_spotprice(year=None):
    import numpy as np
    dates = np.arange(f"{year}-01-01", f"{year+1}-01-01 00:00", dtype="datetime64[h]")
    df = pd.read_excel(SPOT_PATH, index_col=(0))
    df.index = dates
    return df

def load_pypsa_avg(year=None):
    utils.maxnutz()
    import numpy as np
    dates = np.arange(f"{year}-01-01", f"{year+1}-01-01 00:00", dtype="datetime64[h]")
    df = pd.read_csv(MANUTZ_PATH, sep=";", decimal=",", index_col=(0))
    df.index = dates
    return df


def signal_properties(df, separator:float):
    disc = traffo.discretize(df=df, separator=separator)
    anzahl = pd.DataFrame()
    sig = disc.where(disc > 0)
    sig = pd.DataFrame(sig)
    anzahl = sig.count()
    df_step = pd.DataFrame()
    df_not = pd.DataFrame()
    if type(df) == pd.Series:
            df_step = df.shift(1).ne(df).where(df == 1).cumsum()
            df_not = df.shift(1).ne(df).where(df == -1).cumsum()
    elif type(df) == pd.DataFrame:
        for separator in df.columns:
            df_step[separator] = df[separator].shift(1).ne(df[separator]).where(df[separator] == 1).cumsum()
            df_not[separator] = df[separator].shift(1).ne(df[separator]).where(df[separator] == -1).cumsum()

    df_desc = pd.DataFrame()
    df_desc["Zeitraum mit Signal [h]"] = anzahl
    df_desc["Nicht-Signal-Zeitraum [h]"] = len(df) - anzahl
    df_desc["Anzahl Signal-Perioden"] = df_step.max()
    df_desc["Durchschnittliche Dauer Signal [h]"] = (
                df_desc["Zeitraum mit Signal [h]"] / df_desc["Anzahl Signal-Perioden"])
    df_desc["Durchschnittliche Dauer Nicht-Signal [h]"] = df_desc["Nicht-Signal-Zeitraum [h]"] / df_desc[
        "Anzahl Signal-Perioden"]

    return df_desc

def signal_properties_s(df, separator:float):
    disc = traffo.discretize(df=df, separator=separator)
    disc_s = disc.loc[(disc.index.month >= 4) & (disc.index.month < 10)]
    disc_w = disc.loc[(disc.index.month >= 10) | (disc.index.month < 4)]
    anzahl = pd.DataFrame()

    sig_s = disc_s.where(disc_s > 0)
    sig_w = disc_w.where(disc_w > 0)
    sig_s = pd.DataFrame(sig_s)
    sig_w = pd.DataFrame(sig_w)
    df_s = df.loc[(df.index.month >= 4) & (df.index.month < 10)]
    df_w = df.loc[(df.index.month >= 10) | (df.index.month < 4)]

    anzahl_s = sig_s.count()
    anzahl_w = sig_w.count()
    df_step_s = pd.DataFrame()
    df_not_s = pd.DataFrame()
    df_step_w = pd.DataFrame()
    df_not_w = pd.DataFrame()

    if type(df) == pd.Series:
            df_step_s = df_s.shift(1).ne(df_s).where(df_s == 1).cumsum()
            df_not_s = df_s.shift(1).ne(df_s).where(df_s == -1).cumsum()
            df_step_w = df_w.shift(1).ne(df_w).where(df_w == 1).cumsum()
            df_not_w = df_w.shift(1).ne(df_w).where(df_w == -1).cumsum()
    elif type(df) == pd.DataFrame:
        for s in df.columns:
            df_step_s[s] = df_s[s].shift(1).ne(df_s[s]).where(df_s[s] == 1).cumsum()
            df_not_s[s] = df_s[s].shift(1).ne(df_s[s]).where(df_s[s] == -1).cumsum()
            df_step_w[s] = df_w[s].shift(1).ne(df_w[s]).where(df_w[s] == 1).cumsum()
            df_not_w[s] = df_w[s].shift(1).ne(df_w[s]).where(df_w[s] == -1).cumsum()

    df_desc_s = pd.DataFrame()
    df_desc_s["Zeitraum mit Signal [h]"] = anzahl_s
    df_desc_s["Nicht-Signal-Zeitraum [h]"] = len(df_s) - anzahl_s
    df_desc_s["Anzahl Signal-Perioden"] = df_step_s.max()
    df_desc_s["Durchschnittliche Dauer Signal [h]"] = (
                df_desc_s["Zeitraum mit Signal [h]"] / df_desc_s["Anzahl Signal-Perioden"])
    df_desc_s["Durchschnittliche Dauer Nicht-Signal [h]"] = df_desc_s["Nicht-Signal-Zeitraum [h]"] / df_desc_s[
        "Anzahl Signal-Perioden"]
    df_desc_w = pd.DataFrame()
    df_desc_w["Zeitraum mit Signal [h]"] = anzahl_w
    df_desc_w["Nicht-Signal-Zeitraum [h]"] = len(df_w) - anzahl_w
    df_desc_w["Anzahl Signal-Perioden"] = df_step_w.max()
    df_desc_w["Durchschnittliche Dauer Signal [h]"] = (
                df_desc_w["Zeitraum mit Signal [h]"] / df_desc_w["Anzahl Signal-Perioden"])
    df_desc_w["Durchschnittliche Dauer Nicht-Signal [h]"] = df_desc_w["Nicht-Signal-Zeitraum [h]"] / df_desc_w[
        "Anzahl Signal-Perioden"]

    return df_desc_s

def signal_properties_w(df, separator:float):
    disc = traffo.discretize(df=df, separator=separator)

    disc_w = disc.loc[(disc.index.month >= 10) | (disc.index.month < 4)]
    anzahl = pd.DataFrame()

    sig_w = disc_w.where(disc_w > 0)
    sig_w = pd.DataFrame(sig_w)
    df_w = df.loc[(df.index.month >= 10) | (df.index.month < 4)]
    anzahl_w = sig_w.count()

    df_step_w = pd.DataFrame()
    df_not_w = pd.DataFrame()

    if type(df) == pd.Series:
        df_step_w = df_w.shift(1).ne(df_w).where(df_w == 1).cumsum()
        df_not_w = df_w.shift(1).ne(df_w).where(df_w == -1).cumsum()
    elif type(df) == pd.DataFrame:
        for s in df.columns:
            df_step_w[s] = df_w[s].shift(1).ne(df_w[s]).where(df_w[s] == 1).cumsum()
            df_not_w[s] = df_w[s].shift(1).ne(df_w[s]).where(df_w[s] == -1).cumsum()

    df_desc_w = pd.DataFrame()
    df_desc_w["Zeitraum mit Signal [h]"] = anzahl_w
    df_desc_w["Nicht-Signal-Zeitraum [h]"] = len(df_w) - anzahl_w
    df_desc_w["Anzahl Signal-Perioden"] = df_step_w.max()
    df_desc_w["Durchschnittliche Dauer Signal [h]"] = (
            df_desc_w["Zeitraum mit Signal [h]"] / df_desc_w["Anzahl Signal-Perioden"])
    df_desc_w["Durchschnittliche Dauer Nicht-Signal [h]"] = df_desc_w["Nicht-Signal-Zeitraum [h]"] / df_desc_w[
        "Anzahl Signal-Perioden"]

    return df_desc_w