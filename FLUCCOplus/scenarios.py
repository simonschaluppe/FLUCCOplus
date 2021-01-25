
from FLUCCOplus.config import *


@logg
def start_pipeline(df):
    return df.copy()


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