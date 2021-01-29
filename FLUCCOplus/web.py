
from FLUCCOplus.config import *

web_data_path = DATA_RAW / Path("web/WEB-Lastgaenge_03032020_15min_kWh.csv")


@log
def read_web():#All data in kWh
    """All data in kWh"""
    df = pd.read_csv(web_data_path,
                     delimiter=";",
                     index_col="Datetime UCT",
                     parse_dates=["Datetime UCT"],
                     )
    return df #All data in kWh


@logg
def start_pipeline(df):
    return df.copy()

@logg
def clean(df):
    """returns a clean em df 15-17"""
    return (df
            .pipe(start_pipeline)
            .drop("UTCOffset", axis=1)
            .drop("Datetime CET", axis=1)
            .astype(float)
            )
@logg
def power(df):
    """returns the powers in MW"""
    return df.resample("H").sum() / 1000

def adjust_outlier(df):
#     for each column
    pass


@logg
def remove_outliers_wow(df, std=3):
    # keep only the ones that are within +3 to -3 standard deviations in the column 'Data'.
    return df[df.apply(lambda x: np.abs(x - x.mean()) / x.std() < std).all(axis=1)]


@logg
def normalize(df):
    return df.apply(lambda x: x/x.max())