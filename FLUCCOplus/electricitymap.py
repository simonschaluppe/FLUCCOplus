from collections import OrderedDict

from FLUCCOplus.config import *

header_junk = ['production_sources', 'Jahr', 'monat', 'Tag', 'Stunde', 'Datum', 'Tag des Jahres',
               'Tag des Monats', 'Uhrzeit', 'timestamp', 'zone_name']

# Columns of electricity Map 2018-19 and 15-17
common = [
    'total_export_avg',
    'total_import_avg',
    'carbon_intensity_avg',
    'total_consumption_avg',
    'total_production_avg']

# df 15-17
power_origins = [
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
    'power_origin_percent_hydro_discharge_avg']

# df 18-19 only
totals = [
    'total_production_avg',
    'total_storage_avg',
    'total_discharge_avg',
    'total_import_avg',
    'total_export_avg',
    'total_consumption_avg']

power_net_imports = ['power_net_import_CH_avg', 'power_net_import_CZ_avg',
                     'power_net_import_DE_avg', 'power_net_import_HU_avg',
                     'power_net_import_IT-NO_avg', 'power_net_import_SI_avg']

production = [
    'power_production_biomass_avg',
    'power_production_coal_avg',
    'power_production_gas_avg',
    'power_production_hydro_avg',
    'power_production_nuclear_avg',
    'power_production_oil_avg',
    'power_production_solar_avg',
    'power_production_wind_avg',
    'power_production_geothermal_avg',
    'power_production_unknown_avg', ]
consumption = [
    'power_consumption_biomass_avg', 'power_consumption_coal_avg',
    'power_consumption_gas_avg', 'power_consumption_hydro_avg',
    'power_consumption_nuclear_avg', 'power_consumption_oil_avg',
    'power_consumption_solar_avg', 'power_consumption_wind_avg',
    'power_consumption_geothermal_avg', 'power_consumption_unknown_avg',
    'power_consumption_battery_discharge_avg',
    'power_consumption_hydro_discharge_avg']

carbon_intensities = [
    'carbon_intensity_avg',
    'carbon_intensity_production_avg',
    'carbon_intensity_discharge_avg',
    'carbon_intensity_import_avg']
carbon_rate = ['carbon_rate_avg']
carbon_origins = ['carbon_origin_percent_biomass_avg', 'carbon_origin_percent_coal_avg',
                  'carbon_origin_percent_gas_avg', 'carbon_origin_percent_hydro_avg',
                  'carbon_origin_percent_nuclear_avg', 'carbon_origin_percent_oil_avg',
                  'carbon_origin_percent_solar_avg', 'carbon_origin_percent_wind_avg',
                  'carbon_origin_percent_geothermal_avg',
                  'carbon_origin_percent_unknown_avg',
                  'carbon_origin_percent_battery_discharge_avg',
                  'carbon_origin_percent_hydro_discharge_avg', ]
latest_forecasted = [
    'latest_forecasted_dewpoint_avg',
    'latest_forecasted_precipitation_avg',
    'latest_forecasted_solar_avg',
    'latest_forecasted_temperature_avg',
    'latest_forecasted_wind_x_avg',
    'latest_forecasted_wind_y_avg',
    'latest_forecasted_price_avg',
    'latest_forecasted_production_avg',
    'latest_forecasted_consumption_avg',
    'latest_forecasted_power_net_import_CH_avg',
    'latest_forecasted_power_net_import_CZ_avg',
    'latest_forecasted_power_net_import_DE_avg',
    'latest_forecasted_power_net_import_HU_avg',
    'latest_forecasted_power_net_import_IT-NO_avg',
    'latest_forecasted_power_net_import_SI_avg',
    'latest_forecasted_production_solar_avg',
    'latest_forecasted_production_wind_avg']
power_net_discharge = ['power_net_discharge_battery_avg', 'power_net_discharge_hydro_avg']

# aggregate
vars = totals + carbon_intensities

renewables = ["biomass",
              "hydro",
              "solar",
              "wind",
              "geothermal"]

fossile = ["coal",
           "gas",
           "nuclear",
           "oil",
           "unknown"]

discharge = ["battery_discharge",
             "hydro_discharge"]

carriers = renewables + fossile
sources = renewables + fossile + discharge


def col(prefix, vars):
    """what i want: give carrier list with prefix"""
    # return valid col list
    if type(vars) is str:
        return ''.join([prefix, "_", vars, "_avg"])
    else:
        return [''.join([prefix, "_", var, "_avg"]) for var in vars]


pps_RE = col("power_production", renewables)
pps_NRE = col("power_production", fossile)  # no discharge

pcs_RE = col("power_consumption", renewables)
pcs_NRE = col("power_consumption", fossile)
pcs_discharge = col("power_consumption", discharge)

cops_RE = col("carbon_origin_percent", renewables)
cops_NRE = col("carbon_origin_percent", fossile)
cops_discharge = col("carbon_origin_percent", discharge)

pps = pps_RE + pps_NRE
pcs_sources = pcs_RE + pcs_NRE
pcs = pcs_sources + pcs_discharge
cops = cops_RE + cops_NRE + cops_discharge

carrier_colors = {
    "biomass": "xkcd:green",
    "hydro": "xkcd:aqua",
    "solar": "yellow",
    "wind": "xkcd:azure",
    "geothermal": "brown",
    "coal": "darkgray",
    "gas": "xkcd:navy",
    "nuclear": "magenta",
    "oil": "black",
    "unknown": "gray",
    "battery_discharge": "orange",
    "hydro_discharge": "blue"}

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


# %%
@log
def parse_electricity_map():
    df = pd.read_csv("../data/raw/electricityMap/Electricity_map_2015-2019.csv",
                     delimiter=';',
                     parse_dates=["datetime"],
                     index_col="datetime",
                     )
    return df


@log
def read_raw(file):
    """reads a raw electricity map .csv and returns the df"""
    df = pd.read_csv(DATA_RAW / "electricityMap" / file,
                     delimiter=";",
                     parse_dates=["datetime"],
                     index_col="datetime")
    return df



@logg
def start_pipeline(df):
    return df.copy()

@logg
def clean151617(df):
    """returns a clean em df 15-17"""
    return (df
            .pipe(start_pipeline)
            .drop("local_datetime", axis=1)
            .drop
            (
                'datetime,local_datetime,total_production_avg,total_consumption_avg,total_import_avg,total_export_avg,carbon_intensity_avg,power_origin_percent_biomass_avg,power_origin_percent_coal_avg,power_origin_percent_gas_avg,power_origin_percent_hydro_avg,power_origin_percent_nuclear_avg,power_origin_percent_oil_avg,power_origin_percent_solar_avg,power_origin_percent_wind_avg,power_origin_percent_geothermal_avg,power_origin_percent_unknown_avg,'
                'power_origin_percent_hydro_discharge_avg', axis=1)
            .astype(float)
            )


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
def year(df, year: int):
    return df[df.index.year == year]


@logg
def as_df(dict: dict):
    df = pd.concat(dict.values())
    return df

def calc_power_consumption_from_percent(df):
    cols = carriers +["hydro_discharge"]
    for c in cols: #keine discharge (battery, hydro)
        # tc = df["total_consumption_avg"].sum()
        pc = col("power_consumption", c)
        percent = col("power_origin_percent", c)
        df[pc] = df[percent] / 100 * df["total_consumption_avg"]  #wegen%
    df[col("power_consumption", "battery_discharge")] = 0
    return df

@logg
def calc_aggregates(df):
    df["Importe"] = df["total_import_avg"] - df["total_export_avg"]
    df["Wasserkraft"] = df["Laufkraft"] + df["Pumpspeicher"]
    df["Volatile EE"] = df["Laufkraft"] + df["Windkraft"] + df["Photovoltaik"]
    df["Nicht-Volatile"] = df["Stromproduktion"] - df["Wasserkraft"] - df["Windkraft"] - df["Photovoltaik"]
    return df


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


@log
def fetch_1819():
    return (read_raw("Electricity_map_CO2_AT_2018_2019.csv")
            .pipe(start_pipeline)
            .drop(header_junk, axis=1)
            .astype(float)
            )

@log
def preprocess():

    em18 = fetch_1819()

    em15 = (read_raw("Electricity_map_CO2_AT_2015_2017.csv")
            .pipe(start_pipeline)
            .pipe(clean151617)
            .pipe(calc_power_consumption_from_percent)
            )

    em18set = set(em18.columns)
    em15set = set(em15.columns)
    common_cols = sorted(list(em15set & em18set))

    em = pd.concat([em15[common_cols], em18[common_cols]])
    return em


@logg
def save_to_csv(df_dict: dict, scenario_folder="data/scenarios/"):
    from datetime import datetime
    date = datetime.isoformat(datetime.now())[:-10].replace(":", "-")
    folder = scenario_folder + date
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
        # %%
        c = col_dict[col]
        df_scenario[col] = c[scenario_name]

    df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] = df_scenario["Strombedarf"] - df_scenario["Volatile EE"]
    df_scenario["RES1 (RES0-Pumpspeicher)"] = df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] - df_scenario[
        "Pumpspeicher"]
    df_scenario["RES2 (RES1-Nicht-Volatile)"] = df_scenario["RES1 (RES0-Pumpspeicher)"] - df_scenario["Nicht-Volatile"]

    # df_sc["RES0"][scenario_name] = df_scenario["RES0"]
    return df_scenario
