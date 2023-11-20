
from FLUCCOplus.utils import *
import FLUCCOplus.config as config
import FLUCCOplus.conversion_factors as factors


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

RENEWABLES = ["biomass",
              "hydro",
              "solar",
              "wind",
              "geothermal"]

FOSSILE = ["coal",
           "gas",
           "nuclear",
           "oil",
           "unknown"]

DISCHARGE = ["battery_discharge",
             "hydro_discharge"]

CARRIERS = RENEWABLES + FOSSILE
SOURCES = RENEWABLES + FOSSILE + DISCHARGE

def col(prefix, vars, suffix="_avg"):
    """what i want: give variable (carrier) list with prefix"""
    # return valid col list
    if type(vars) is str:
        return ''.join([prefix, "_", vars, suffix])
    else:
        return [''.join([prefix, "_", var, suffix]) for var in vars]

pp = "power_production"
pps_RE = col(pp, RENEWABLES)
pps_NRE = col(pp, FOSSILE)  # no discharge

pc = "power_consumption"
pcs_RE = col(pc, RENEWABLES)
pcs_NRE = col(pc, FOSSILE)
pcs_discharge = col(pc, DISCHARGE)

cop = "carbon_origin_percent"
cops_RE = col(cop, RENEWABLES)
cops_NRE = col(cop, FOSSILE)
cops_discharge = col(cop, DISCHARGE)

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


def _read_raw(from_path):
    return pd.read_csv(from_path,
                       delimiter=";",
                       parse_dates=["datetime"],
                       index_col="datetime")

@log
def read_raw(file):
    """
    reads a raw electricity map .csv from the data/raw/electricitymap folder
    :returns: df
    """
    return _read_raw(config.DATA_RAW / "electricityMap" / file)


def _read_interim(from_path):
    return pd.read_csv(from_path,
                       delimiter=";",
                       parse_dates=["datetime"],
                       index_col="datetime",
                       decimal=",",
                       encoding="cp850"
                       )

@log
def read_interim(file, encoding="cp850"):
    return _read_interim(config.DATA_INTERIM / file)


@logg
def start_pipeline(df):

    return df.copy()

def fill_values(df):
    return df.resample('H').ffill()

def del_29febr(df):
    return df.drop(df.index[1416:1440])

@logg
def clean151617(df):
    """returns a clean em df 15-17"""
    return (df
            .drop("local_datetime", axis=1)
            .drop
            (
                'datetime,local_datetime,total_production_avg,total_consumption_avg,'
                'total_import_avg,total_export_avg,'
                'carbon_intensity_avg,power_origin_percent_biomass_avg,power_origin_percent_coal_avg,power_origin_percent_gas_avg,power_origin_percent_hydro_avg,power_origin_percent_nuclear_avg,power_origin_percent_oil_avg,power_origin_percent_solar_avg,power_origin_percent_wind_avg,power_origin_percent_geothermal_avg,power_origin_percent_unknown_avg,'
                'power_origin_percent_hydro_discharge_avg', axis=1)
            .pipe(fill_values)
            .astype(float)
            )



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

@logg
def calc_power_consumption_from_percent(df):
    cols = CARRIERS + ["hydro_discharge"]
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

@log
def fetch_20():
    """
    returns the cleaned elmap dataset from 2018 and 2019:
    :return:
    """
    return (_read_raw("../data/raw/electricityMap/AT_2020.csv")

            .pipe(start_pipeline)
            .drop(header_junk, axis=1)
            .pipe(fill_values)
            .pipe(del_29febr)
            .astype(float)
            )

@log
def fetch_1819():
    """
    returns the cleaned elmap dataset from 2018 and 2019:
    :return:
    """
    return (_read_raw("../data/raw/electricityMap/Electricity_map_CO2_AT_2018_2019.csv")
            .pipe(start_pipeline)
            .drop(header_junk, axis=1)
            .pipe(fill_values)
            .astype(float)
            )

@log
def fetch_151617():
    """
    returns the cleaned elmap dataset from 2015-2017: but there is alot of dropping
    :return:
    """
    return (_read_raw("../data/raw/electricityMap/Electricity_map_CO2_AT_2015_2017.csv")
            .pipe(start_pipeline)
            .pipe(clean151617)
            .pipe(calc_power_consumption_from_percent)
            )



@log
def preprocess():
    """
    returns a df with all columns common to elmap1819 and elmap15-17
    """
    em18 = fetch_1819()

    em15 = fetch_151617()

    em18set = set(em18.columns)
    em15set = set(em15.columns)
    common_cols = sorted(list(em15set & em18set))

    em = pd.concat([em15[common_cols], em18[common_cols]])
    return em


@log
def fetch_common():
    return _read_interim("../data/interim/em_common_15-19.csv")

@log
def fetch(year=None, common=False):
    if year:
        if 2019 >= year >= 2018:
            df = fetch_1819()
        elif 2015 <= year <= 2017:
            df = fetch_151617()
        elif 2020:
            df = fetch_20()
        return df[df.index.year == year]

    elif common:
        return fetch_common()

    else:
        raise AttributeError("Need to specify a parameter: year or common=True!")

@logg
def drop_suffixes(df):
    print("not implemented yet")
    return df


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


def get(year, column, set_name=None):
    """returns a given column of a given year as a series, optionally renamed"""
    if year in [2015,2016,2017]:
        df = fetch_151617()
    elif year in [2018, 2019]:
        df = fetch_1819()
    else:
        raise ValueError(f"Year must be in [2015-2019] as int, got {year}")
    series = df[df.index.year == year][column]
    if set_name:
        series.rename(set_name, inplace=True)
    return series

def annual_emissions():
    """returns a series of electricity map co2 averages based on the resampled dataframe"""
    df = read_interim("em_common_15-19.csv")

    avg = pd.Series([df.loc[df.index.year == y, "carbon_intensity_avg"].mean() for y in df.index.year.unique()], index=[df.index.year.unique()])
    avg.index = ["Elmap "+str(i) for i in range(2015,2020)]

    avg["Elmap 2015-2018"] = df.loc[df.index.year!=2019, "carbon_intensity_avg"].mean()
    avg["Elmap 2015-2019"] = df[ "carbon_intensity_avg"].mean()
    avg["OIB RL6  '18"] = 248
    avg["OIB RL6-E'19"] = 227

    return avg


def plot_PE_factors_OIB():
    pd.DataFrame(factors.PE_factors_OIB2019) \
        .drop(["fPE"]) \
        .transpose() \
        .plot(kind="bar", color=["grey", "lightgreen"], stacked=True)


def primary_energy(df, type="Primärenergiefaktor total [MJ-eq]"):
    """

    :parameter
    :paramter type: default CONVERSION_FACTORS has  "Primärenergiefaktor total [MJ-eq]"
                    'Primärenergiefaktor fossil [MJ-eq]'
                    'Primärenergiefaktor nuklear  [MJ-eq]'
                    'Primärenergiefaktor total erneuerbar [MJ-eq]'
                    'Primärenergiefaktor Abwärme / Abfall [MJ-eq]'
                    'CO2-Äquivalente  [kg CO2-eq]'
                    'Kohlendioxid, fossil [kg CO2-eq]'
                    "Umweltbelastungspunkte [UBP'13]"
    """
    for src in SOURCES:
        src_mapping = factors.conversion_mapping[src]
        if src not in df.columns:
            raise KeyError(f"{src=} not in {df.columns=}, \nneeds conversion to  ")
        df[src] = df[src] * factors.CONVERSION_FACTORS[src_mapping][type]
    df["total_consumption_avg"] = df.sum(axis=1)
    return df

def pe_factors(df, totals="total_consumption_avg"):
    """returns"""
    df = fetch_common().rename(columns={a: b for a, b in zip(pcs, SOURCES)})
    PE = primary_energy(df[SOURCES], type="Primärenergiefaktor total [MJ-eq]")
    fPE = PE[totals] / df[totals]

    PEnern = primary_energy(df[SOURCES], type="Primärenergiefaktor fossil [MJ-eq]")
    fPEnern = PEnern[totals] / df[totals]

    PEern = primary_energy(df[SOURCES], type="Primärenergiefaktor total erneuerbar [MJ-eq]")
    fPEern = PEern[totals] / df[totals]

    PEnukl = primary_energy(df[SOURCES], type="Primärenergiefaktor nuklear  [MJ-eq]")
    fPEnukl = PEnukl[totals] / df[totals]

    PEabw = primary_energy(df[SOURCES], type="Primärenergiefaktor Abwärme / Abfall [MJ-eq]")
    fPEabw = PEabw[totals] / df[totals]
    return pd.DataFrame({"fPE":fPE,
                         "fPE,n.ern.":fPEnern,
                         "fPE,ern.":fPEern,
                         "fPE,nukl.":fPEnukl,
                         "fPE,abw.":fPEabw,
                         }
                        )

def pe_consumption():
    df = fetch_common().rename(columns={a: b for a, b in zip(pcs, SOURCES)})
    totals = "total_consumption_avg"
    #TODO: implement

def pe_production():
    df = fetch_1819().rename(columns={a: b for a, b in zip(pps, CARRIERS)})
    pp = "total_production_avg"
    #TODO: implement


if __name__ == "__main__":
    df = fetch_common()
    pe = pe_factors(df)



