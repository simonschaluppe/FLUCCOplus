import pandas as pd
import numpy as np

import FLUCCOplus.utils as utils
import FLUCCOplus.config as config
import FLUCCOplus.web as web
import FLUCCOplus.transform as traffo
from pathlib import Path

PEEXCEL_PATH = config.DATA_PROCESSED / Path("peexcel_normalized.csv")
WEB_PATH = config.DATA_PROCESSED / Path("WEB_normalized.csv")
SPOT_PATH = config.DATA_PROCESSED / Path("DrexelCO2/Signale_CO2mix_SpotMarket.xlsx")
MANUTZ_PATH = config.DATA_PROCESSED / Path("MANutz/maxnutz_normalized.csv")
RESLOAD18_PATH = config.DATA_INTERIM / Path("Residuallast.csv")
RESLOAD19_PATH = config.DATA_INTERIM / Path("RES0-40-55.csv")

def load_peexcel():
    return pd.read_csv(PEEXCEL_PATH, index_col=0, parse_dates=True)

def load_web(year=None):
    df = web.read(WEB_PATH, decimal=",")
    if year:
        df = df[df.index.year==year]
    return df

def load_spotprice(year=2018):
    df = pd.read_excel(SPOT_PATH, index_col=(0))
    df = utils.set_datetime_index(df, year)
    return df

def load_pypsa_avg(year=2018):
    utils.maxnutz()
    df = pd.read_csv(MANUTZ_PATH, sep=";", decimal=",", index_col=(0))
    df = utils.set_datetime_index(df, year)
    return df
    
def load_resload_discretized_signals(year=2018):
    path = RESLOAD18_PATH if year == 2018 else RESLOAD19_PATH
    df = pd.read_csv(path, sep=";", decimal=",", index_col=(0))
    df.index = utils.set_datetime_index(df, year)
    return df

def load_all(year=2018):
    """
    Loads all signals from peexcel, W.E.B.,  and PyPSA.
    
    Parameters:
    year (int, optional): Year to filter WEB data, other signals are just set to that date 
                          If None, data is loaded without filtering by year.
    
    Returns:
    pd.DataFrame: A concatenated dataframe of all inputs, aligned on the index.
    """
    # Load data from individual functions
    peexcel_df = load_peexcel()
    web_df = load_web(year=year)
    pypsa_avg_df = load_pypsa_avg(year=year)

    # Concatenate all dataframes along the columns, aligning on the index
    all_data = pd.concat([peexcel_df, web_df,pypsa_avg_df], axis=1)

    # Handle missing data (e.g., fill missing values or leave as NaN)
    # For this example, we leave NaN values as-is; modify as needed:
    # all_data = all_data.fillna(0)  # Example: fill missing values with 0

    return all_data



def signal_points_from_series(series):
    count = 0
    ds = 0
    dn = 0
    prev = 1
    hour = 0
    signals = [(0,0,0)]
    for hour, i in enumerate(series):
        if i == prev: # keep counting
            if i == 1:
                ds += 1
            else:
                dn += 1
        if i != prev:
            if i == 1:
                count += 1
                signals.append((hour, dn, ds))
                ds = 1
                dn = 0
            else:
                dn+=1
        prev = i
            
    return signals

def get_signal_points_as_df(signal_df):
    result_dfs = []

    for col in signal_df.columns:
        signals = signal_points_from_series(signal_df[col])  # Extract signals
        _, dn, ds = zip(*signals)  # Unpack the signals into dn and ds

        # Create a dataframe with dn and ds
        dfs = pd.DataFrame({"h": range(len(dn)), "dn": dn, "ds": ds})
        dfs["name"] = col  # Add a column for the column name

        # Append to the result list
        result_dfs.append(dfs)
    
    final_df = pd.concat(result_dfs, ignore_index=True)
    return final_df



def find_cutoff(series, ratio):
    """
    Finds a cutoff for the series such that the number of elements greater than it
    equals `ratio * len(series)`.

    Parameters:
    series (pd.Series): Input series of values.
    ratio (float): Fraction of the series size (0 < x <= 1).

    Returns:
    float: The "cutoff" value that meets the condition.
    """
    # Sort the series in descending order
    sorted_series = series.sort_values(ascending=False)
    
    # Determine the index corresponding to x * series size
    threshold_index = int(ratio * len(series))
    
    # Handle edge case when x * len(series) is 0 or exceeds series size
    if threshold_index == 0:
        raise ValueError("x * series size is too small; no elements satisfy the condition.")
    if threshold_index > len(series):
        raise ValueError("x * series size exceeds the series length.")

    # Find the value at the threshold index
    cutoff = sorted_series.iloc[threshold_index - 1]
    return cutoff

def discretize_dynamic(df_or_series, ratio=0.5):
    """
    Discretize a Signal for Series or DataFrame based on desired Duration-Ratio of Signal to Non-Signal.

    Parameters:
    data (pd.Series or pd.DataFrame): Input data to process.
    ratio (float): Duration-Ratio of Signal to Non-Signal: 0.3 means 30% of Hours will have Signal

    Returns:
    pd.Series or pd.DataFrame: Discretized Series or DataFrame.
    """
    if isinstance(df_or_series, pd.Series):
        # Handle Series
        cutoff = find_cutoff(df_or_series, ratio)
        return traffo.discretize(df_or_series, cutoff)
    elif isinstance(df_or_series, pd.DataFrame):
        # Handle DataFrame
        results = {}
        for col in df_or_series.columns:
            series = df_or_series[col]
            cutoff = find_cutoff(series, ratio)
            results[col] = traffo.discretize(series, cutoff)
        return pd.DataFrame(results, index=df_or_series.index)
    else:
        raise ValueError("Input must be a Pandas Series or DataFrame")
    


def signal_properties(df, separator:float):
    disc = traffo.discretize(df=df, separator=separator)
    anzahl = pd.DataFrame()
    sig = disc.where(disc > 0)
    sig = pd.DataFrame(sig)
    anzahl = sig.count()
    df_step = pd.DataFrame()
    df_not = pd.DataFrame()
    if type(df) == pd.Series:
            df_step = df.shift(1).ne(df).where(df == df.max()).cumsum()
            df_not = df.shift(1).ne(df).where(df == df.min()).cumsum()
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
            df_step_s = df_s.shift(1).ne(df_s).where(df_s == df_s.max()).cumsum()
            df_not_s = df_s.shift(1).ne(df_s).where(df_s == df_s.min()).cumsum()
            df_step_w = df_w.shift(1).ne(df_w).where(df_w == df_w.max()).cumsum()
            df_not_w = df_w.shift(1).ne(df_w).where(df_w == df_w.min()).cumsum()
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

    return df_desc_s, df_desc_w

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

