
import FLUCCOplus.config as config
from FLUCCOplus.utils import *



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


@log
def all():
    sc = (read("szenarien_w2s.xlsx")
          .pipe(start_pipeline)
          .pipe(NaNtoZero)
          .pipe(format_df)
          .pipe(convert_PJ_to_GWH)
          )
    return sc


@log
def factors(source, target, scenarios):
    """

    :param source: String or Index int of source scenario
    :param target: String or Index int of target scenario
    :param scenarios: Dataframe with Scenarios, must include all EM_TO_EXCEL_colnames
    :return: dict with factors for all EM_TO_EXCEL_colnames
    """
    if type(source) == int:
        src = scenarios.index[source]
    else: src = source

    if type(target) == int:
        tgt = scenarios.index[target]
    else: tgt = target

    carriers = EM_TO_EXCEL_colnames.values()
    f = scenarios.loc[tgt, carriers] / scenarios.loc[src, carriers]
    factors = {"source": src, "target": tgt}
    factors.update({i: j for i, j in zip(carriers, f)})

    return factors


class Scenario:
    name:str
