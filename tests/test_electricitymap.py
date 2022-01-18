import os

import pytest
from FLUCCOplus import electricitymap as elmap


@pytest.mark.parametrize("var", elmap.CARRIERS)
@pytest.mark.parametrize("prefix, result", [
                         ("power_production", elmap.production)])
def test_cols(prefix, var, result):
    assert elmap.col(prefix, var) in result

def test_col():
    assert elmap.col("power_production", "gas") == "power_production_gas_avg"

def test_pps():
    assert elmap.pps_RE == elmap.col("power_production", elmap.RENEWABLES)
    assert elmap.pps_NRE == elmap.col("power_production", elmap.FOSSILE)  # no discharge


@pytest.fixture(scope="session")
def raw_df():
    return elmap._read_raw("data/raw/electricityMap/Electricity_map_CO2_AT_2018_2019.csv")


def test_read_raw(raw_df):
    assert raw_df.shape == (17505, 83)

