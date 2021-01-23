import sys
import pandas as pd


def parse_econtrol(path):
    df = pd.read_excel(path, sheet_name="FLUCCOplus",skiprows=[1],index_col=0)
    clean_colnames = ["".join([c for c in col if c not in "()\n- ,="]) for col in df.columns]
    df.rename(columns=dict(zip(df.columns, clean_colnames)), inplace=True)
    return df

def parse_electricitymap(path)

if __name__ == "__main__":
    ec = parse_econtrol("data/e-control/BStGes-JR1_Bilanz.xlsx")
