import pytest
import FLUCCOplus.electricitymap as elmap
from FLUCCOplus.utils import *

@pytest.mark.parametrize("var", elmap.carriers)
@pytest.mark.parametrize("prefix, result", [
                         ("power_production", elmap.production)])
def test_cols(prefix, var, result):
    assert elmap.col(prefix, var) in result

def test_col():
    assert elmap.col("power_production", "gas") == "power_production_gas_avg"

def test_pps():
    assert elmap.pps_RE == elmap.col("power_production", elmap.renewables)
    assert elmap.pps_NRE == elmap.col("power_production", elmap.fossile)  # no discharge


@pytest.fixture(scope="session")
def raw_df():
    return elmap.read_raw("Electricity_map_CO2_AT_2018_2019.csv")


def test_read_raw(raw_df):
    assert raw_df.shape == (17505, 83)

def test_preprocess():
    assert elmap.preprocess().shape == (43809, 17)


# @logg
# def start_pipeline(df):
#     return df.copy()
#
# @logg
# def clean151617(df):
#     """returns a clean em df 15-17"""
#     return (df
#             .pipe(start_pipeline)
#             .drop("local_datetime", axis=1)
#             .drop
#             (
#                 'datetime,local_datetime,total_production_avg,total_consumption_avg,total_import_avg,total_export_avg,carbon_intensity_avg,power_origin_percent_biomass_avg,power_origin_percent_coal_avg,power_origin_percent_gas_avg,power_origin_percent_hydro_avg,power_origin_percent_nuclear_avg,power_origin_percent_oil_avg,power_origin_percent_solar_avg,power_origin_percent_wind_avg,power_origin_percent_geothermal_avg,power_origin_percent_unknown_avg,'
#                 'power_origin_percent_hydro_discharge_avg', axis=1)
#             .astype(float)
#             )
#
#
# @logg
# def rename_cols_to_common(df):
#     df = df.rename(columns=EM_TO_EXCEL_colnames)
#     return df
#
#
#
# @log
# def split_into_years(df):
#     """separate dataframe in dict(year: df[year]"""
#     years = df.index.year.unique().values
#     # print(f"{len(years)} Jahre: ", years)
#     # #%%
#     # for i, year in enumerate(years):
#     df_dict = {year: df_slice for year, df_slice in zip(years, [df[df.index.year == y] for y in years])}
#     return df_dict
#
#
# @logg
# def year(df, year: int):
#     return df[df.index.year == year]
#
#
# @logg
# def as_df(dict: dict):
#     df = pd.concat(dict.values())
#     return df
#
# def calc_power_consumption_from_percent(df):
#     cols = carriers +["hydro_discharge"]
#     for c in cols: #keine discharge (battery, hydro)
#         # tc = df["total_consumption_avg"].sum()
#         pc = col("power_consumption", c)
#         percent = col("power_origin_percent", c)
#         df[pc] = df[percent] / 100 * df["total_consumption_avg"]  #wegen%
#     df[col("power_consumption", "battery_discharge")] = 0
#     return df
#
# @logg
# def calc_aggregates(df):
#     df["Importe"] = df["total_import_avg"] - df["total_export_avg"]
#     df["Wasserkraft"] = df["Laufkraft"] + df["Pumpspeicher"]
#     df["Volatile EE"] = df["Laufkraft"] + df["Windkraft"] + df["Photovoltaik"]
#     df["Nicht-Volatile"] = df["Stromproduktion"] - df["Wasserkraft"] - df["Windkraft"] - df["Photovoltaik"]
#     return df
#
#
# @logg
# def scale_to_scenario(df, factors):
#     """takes a EM dataframe and scaling factors and returns a dict with keys [scenario]:  vals [scaled dataframes]"""
#     scens = OrderedDict()
#     columns = sorted(list(EXCEL_TO_EM_colnames.keys()))
#     for i, sc in enumerate(factors.index):
#         scens[sc] = df[columns].copy()
#         for col in columns:
#             f = factors[col][i]
#             year = factors["EM"][i]
#             scens[sc].loc[scens[sc].index.year == year, col] = df.loc[df.index.year == year, col] * f
#
#         scens[sc]["RES0 (Bedarf-PV,Wind,Laufkraft)"] = scens[sc]["Strombedarf"] - scens[sc]["Volatile EE"]
#         scens[sc]["RES1 (RES0-Pumpspeicher)"] = scens[sc]["RES0 (Bedarf-PV,Wind,Laufkraft)"] - scens[sc][
#             "Pumpspeicher"]
#         scens[sc]["RES2 (RES1-Nicht-Volatile)"] = scens[sc]["RES1 (RES0-Pumpspeicher)"] - scens[sc][
#             "Nicht-Volatile"]
#     return scens
#
#
# @log
# def fetch_1819():
#     return (read_raw("Electricity_map_CO2_AT_2018_2019.csv")
#             .pipe(start_pipeline)
#             .drop(header_junk, axis=1)
#             .astype(float)
#             )
#
# @log
# def preprocess():

#
# @logg
# def save_to_csv(df_dict: dict, scenario_folder="data/scenarios/"):
#     from datetime import datetime
#     date = datetime.isoformat(datetime.now())[:-10].replace(":", "-")
#     folder = scenario_folder + date
#     import os
#     os.mkdir(folder)
#     for name, df in df_dict.items():
#         df.to_csv("".join([folder, "/", name, "MW.csv"]),
#                   sep=";",
#                   decimal=",",
#                   encoding="cp850")
#
#         print(name, " saved!")
#
#
# @logg
# def get_scenario(scenario_name, col_dict, Excel_to_EM_dict):
#     """gets the preprocessed scenario including residual loads"""
#     df_scenario = pd.DataFrame()
#
#     for col in Excel_to_EM_dict.keys():
#         # %%
#         c = col_dict[col]
#         df_scenario[col] = c[scenario_name]
#
#     df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] = df_scenario["Strombedarf"] - df_scenario["Volatile EE"]
#     df_scenario["RES1 (RES0-Pumpspeicher)"] = df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] - df_scenario[
#         "Pumpspeicher"]
#     df_scenario["RES2 (RES1-Nicht-Volatile)"] = df_scenario["RES1 (RES0-Pumpspeicher)"] - df_scenario["Nicht-Volatile"]
#
#     # df_sc["RES0"][scenario_name] = df_scenario["RES0"]
#     return df_scenario
