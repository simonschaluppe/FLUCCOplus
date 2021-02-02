
import FLUCCOplus.config as config
from FLUCCOplus.utils import *


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


@log
def read(path):
    from FLUCCOplus.config import DATA_RAW
    return pd.read_excel(DATA_RAW / "szenarien"/ path,
                  sheet_name="scenarios",
                  index_col=0, skiprows=range(1, 3))

@logg
def start_pipeline(df):
    return df.copy()

@logg
def rename_cols_to_common(df):
    df = df.rename(columns=EM_TO_EXCEL_colnames)
    return df



@logg
def convert_PJ_to_GWH(df):
    jahr = df["Jahr"]
    df = df.drop("Jahr", axis=1)
    df = df * PJ_TO_GWH
    df.insert(0,"Jahr", jahr)
    df.index.rename("Szenario", inplace=True)
    return df

@logg
def NaNtoZero(df):
    return df.fillna(0)

@logg
def format_df(df):
    return df.astype({"Jahr":"int32"})


@logg
def get_scenario(scenario_name, col_dict, Excel_to_EM_dict):
    """gets the preprocessed scenario including residual loads"""
    df_scenario = pd.DataFrame()

    for col in Excel_to_EM_dict.keys():
        # %%
        c = col_dict[col]
        df_scenario[col] = c[scenario_name]

    df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] = df_scenario["Strombedarf"] - df_scenario["Volatile EE"]
    df_scenario["RES1 (RES0-Pumpspeicher)"] = df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] - df_scenario[
        "Pumpspeicher"]
    df_scenario["RES2 (RES1-Nicht-Volatile)"] = df_scenario["RES1 (RES0-Pumpspeicher)"] - df_scenario["Nicht-Volatile"]

    # df_sc["RES0"][scenario_name] = df_scenario["RES0"]
    return df_scenario
