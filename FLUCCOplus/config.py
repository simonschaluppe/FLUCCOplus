
# imports


from FLUCCOplus.utils import *


# Configuration Parameters

VERBOSE = True

DATA_RAW = Path("../data/raw")
DATA_EXTERNAL = Path("../data/external")
DATA_INTERIM = Path("../data/interim")
DATA_PROCESSED = Path("../data/processed")

SAVE_CSV_FORMAT = {
    "sep": ";",
    "decimal": ",",
    "encoding": "cp850"
}


# Debuggung

if VERBOSE:
    print(__name__, " loaded!")
