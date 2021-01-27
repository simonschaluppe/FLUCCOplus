


from FLUCCOplus.config import *

web_data_path = DIR_DATA_RAW / Path("web/WEB-Lastgaenge_03032020_15min_kWh.csv")


@log
def read_web():
    df = pd.read_csv(web_data_path,
                     delimiter=";",
                     index_col="Datetime UCT",
                     parse_dates=True)
    return df

#All data in kWh

