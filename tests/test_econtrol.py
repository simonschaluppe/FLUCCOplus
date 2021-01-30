import pytest

import FLUCCOplus.econtrol as ec

def test_parse_econtrol():
    pass
    # df = pd.read_excel(path, sheet_name="FLUCCOplus",skiprows=[1],index_col=0)
    # return df

def test_clean_colnames():
    pass
    # clean_colnames = ["".join([c for c in col if c not in "()\n- ,="]) for col in df.columns]
    # dfreturn = df.rename(columns=dict(zip(df.columns, clean_colnames)))
    # return dfreturn


def test_plot_stacked():
    pass
    # import matplotlib.pyplot as plt
    # df.plot.bar(stacked=True)
    # plt.show()
    # return df

def test_production():
    # return df
    pass


#test pandas
# pd.testing.assert_frame_equal(actual, expected)