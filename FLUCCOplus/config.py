
# imports

from pathlib import Path

# Configuration Parameters

VERBOSE = True

import logging
logging.basicConfig(
    # filename  = 'app.log',      # Log output file
    level     = logging.DEBUG,   # Output level
)



DATA_RAW = Path("../data/raw")
DATA_EXTERNAL = Path("../data/external")
DATA_INTERIM = Path("../data/interim")
DATA_PROCESSED = Path("../data/processed")

SAVE_CSV_FORMAT = {
    "sep": ";",
    "decimal": ",",
    "encoding": "cp850" #so windows excel gets it
}


# Debuggung

if VERBOSE:
    print(__name__, " loaded!")
