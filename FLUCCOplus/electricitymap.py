
import pandas as pd
from collections import OrderedDict



from FLUCCOplus.config import *

headers = ['Source', 'Series_name', 'Jahr',
    'monat', 'woche', 'Tag', 'Stunde',
    'Datum', 'Tag des Jahres', 'Tag des Monats',
    'Stunde des jahres',
    'Uhrzeit', 'timestamp', 'zone_name',]

carbon = ['carbon_intensity_avg',
    'carbon_intensity_production_avg',
    'carbon_intensity_discharge_avg',
    'carbon_intensity_import_avg',
    'carbon_rate_avg']

EM_RAW_COLS = headers + \
              carbon + \
              [
    'total_production_avg',
    'total_storage_avg',
    'total_discharge_avg',
    'total_import_avg',
    'total_export_avg',
    'total_consumption_avg',

    'power_production_biomass_avg',
    'power_production_coal_avg',
    'power_production_gas_avg',
    'power_production_hydro_avg',
    'power_production_nuclear_avg',
    'power_production_oil_avg',
    'power_production_solar_avg',
    'power_production_wind_avg',
    'power_production_geothermal_avg',
    'power_production_unknown_avg',

    'power_origin_percent_biomass_avg',
    'power_origin_percent_coal_avg',
    'power_origin_percent_gas_avg',
    'power_origin_percent_hydro_avg',
    'power_origin_percent_nuclear_avg',
    'power_origin_percent_oil_avg',
    'power_origin_percent_solar_avg',
    'power_origin_percent_wind_avg',
    'power_origin_percent_geothermal_avg',
    'power_origin_percent_unknown_avg',
    'power_origin_percent_hydro_discharge_avg'
              ]


EM_TO_EXCEL_colnames = {
            "power_production_wind_avg":    "Windkraft",
            "power_production_solar_avg":   "Photovoltaik",
            "power_production_hydro_avg":   "Laufkraft",
            "total_consumption_avg":        "Strombedarf",
            "total_production_avg":         "Stromproduktion",
            "power_consumption_hydro_discharge_avg": "Pumpspeicher"}

EXCEL_TO_EM_colnames = {v:k for k, v in EM_TO_EXCEL_colnames.items()}
EXCEL_TO_EM_colnames["Volatile EE"] = "power_production_volatile_avg"
EXCEL_TO_EM_colnames["Nicht-Volatile"] = "power_production_non-volatile_avg"
EXCEL_TO_EM_colnames["Pumpspeicher"] = "power_consumption_hydro_discharge_avg"
EXCEL_TO_EM_colnames["Wasserkraft"] = "power_production_hydro_and_discharge_avg"

#%%
@log
def read_electricity_map():
    df = pd.read_csv("../data/electricityMap/Electricity_map_2015-2019.csv",
                     delimiter=';',
                     parse_dates=["datetime"],
                     index_col="datetime")
    return df

@logg
def start_pipeline(df):
    return df.copy()

@logg
def rename_cols_to_common(df):
    df = df.rename(columns=EM_TO_EXCEL_colnames)
    return df


@log
def split_into_years(df):
    """separate dataframe in dict(year: df[year]"""
    years = df.index.year.unique().values
    # print(f"{len(years)} Jahre: ", years)
    # #%%
    # for i, year in enumerate(years):
    df_dict = {year: df_slice for year, df_slice in zip(years, [df[df.index.year == y] for y in years])}
    return df_dict


@logg
def calc_aggregates(df):
    df["Importe"] = df["total_import_avg"] - df["total_export_avg"]
    df["Wasserkraft"] = df["Laufkraft"] + df["Pumpspeicher"]
    df["Volatile EE"] = df["Laufkraft"] + df["Windkraft"] + df["Photovoltaik"]
    df["Nicht-Volatile"] = df["Stromproduktion"] - df["Wasserkraft"] - df["Windkraft"] - df["Photovoltaik"]
    return df

# df = prepare_EM_df(path="data/EM1819RESL_2021-01-11.csv")
# #%%
# df_PJ = df.groupby(
#     [df.index.year])[excel_cols].sum()/1000/PJ_TO_GWH
# df_PJ
#
# #%% md
#

#%%

# from datetime import datetime
# date = datetime.isoformat(datetime.now())[:-16]
#
# df_PJ.to_csv(''.join(["data/EM1819scenarios_Annual_PJ_",date,".csv"]),
#              sep=";",
#              decimal=",",
#              encoding="cp850")



#%%
@logg
def scale_to_scenario(df, factors):
    """takes a EM dataframe and scaling factors and returns a dict with keys [scenario]:  vals [scaled dataframes]"""
    scens = OrderedDict()
    columns = sorted(list(EXCEL_TO_EM_colnames.keys()))
    for i, sc in enumerate(factors.index):
        scens[sc] = df[columns].copy()
        for col in columns:
            f = factors[col][i]
            year = factors["EM"][i]
            scens[sc].loc[scens[sc].index.year == year, col] = df.loc[df.index.year == year, col] * f


        scens[sc]["RES0 (Bedarf-PV,Wind,Laufkraft)"] = scens[sc]["Strombedarf"] - scens[sc]["Volatile EE"]
        scens[sc]["RES1 (RES0-Pumpspeicher)"] = scens[sc]["RES0 (Bedarf-PV,Wind,Laufkraft)"] - scens[sc][
            "Pumpspeicher"]
        scens[sc]["RES2 (RES1-Nicht-Volatile)"] = scens[sc]["RES1 (RES0-Pumpspeicher)"] - scens[sc][
            "Nicht-Volatile"]
    return scens


@logg
def save_to_csv(df_dict:dict, scenario_folder="data/scenarios/"):
    from datetime import datetime
    date = datetime.isoformat(datetime.now())[:-10].replace(":", "-")
    folder =  scenario_folder + date
    import os
    os.mkdir(folder)
    for name, df in df_dict.items():
        df.to_csv("".join([folder, "/", name, "MW.csv"]),
                           sep=";",
                           decimal=",",
                           encoding="cp850")

        print(name, " saved!")


@logg
def get_scenario(scenario_name, col_dict, Excel_to_EM_dict):
    """gets the preprocessed scenario including residual loads"""
    df_scenario = pd.DataFrame()

    for col in Excel_to_EM_dict.keys():
        #%%
        c = col_dict[col]
        df_scenario[col] = c[scenario_name]

    df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] = df_scenario["Strombedarf"] - df_scenario["Volatile EE"]
    df_scenario["RES1 (RES0-Pumpspeicher)"] = df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] - df_scenario["Pumpspeicher"]
    df_scenario["RES2 (RES1-Nicht-Volatile)"] = df_scenario["RES1 (RES0-Pumpspeicher)"] - df_scenario["Nicht-Volatile"]

    # df_sc["RES0"][scenario_name] = df_scenario["RES0"]
    return df_scenario


