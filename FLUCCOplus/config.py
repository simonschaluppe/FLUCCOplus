
# imports

from pathlib import Path

# Configuration Parameters

VERBOSE = True

import logging
logging.basicConfig(
    filename  = 'app.log',      # Log output file
    level     = logging.DEBUG,   # Output level
)

MODULE_DIR = Path(__file__).parent.parent.resolve()
DATA_PATH = MODULE_DIR / Path("data")

DATA_RAW = DATA_PATH / "raw"
DATA_EXTERNAL = DATA_PATH / "external"
DATA_INTERIM = DATA_PATH / "interim"
DATA_PROCESSED = DATA_PATH / "processed"

PLOTS = DATA_PATH / "Plots"




SAVE_CSV_FORMAT = {
    "sep": ";",
    "decimal": ",",
    "encoding": "cp850" #so windows excel gets it
}

DPI = 220 # image quality

COLORS = {
    'Laufkraft': "blue",
    'Windkraft': "cyan",
    'Photovoltaik': "orange",
    'Pumpspeicher': "lightblue",
    'Nicht-Volatile': "darkgrey",
    "Strombedarf": "black",
    "Volatile EE": "green",
    "Erzeugung": "green"
}

ENERGIES = {
    "Strombedarf": {
        "de": "Strombedarf",
        "en": "Electricity Demand",
        "color": "black"
    },
    "Laufkraft": {
        "de": "Wasser-Laufkraft",
        "en": "Hydro (ROR)",
        "color": "blue"
    },
    "Windkraft": {
        "de": "Windkraft",
        "en": "Wind Power",
        "color": "cyan"
    },
    "Photovoltaik": {
        "de": "Photovoltaik",
        "en": "Photovoltaics",
        "color": "orange"
    },
    "Pumpspeicher": {
        "de": "Wasserkraft-Pumpspeicher",
        "en": "Hydro (Pumped)",
        "color": "lightblue"
    },
    "Nicht-Volatile": {
        "de": "Nicht-Volatile",
        "en": "Non-Volatile RES",
        "color": "darkgrey"
    },
    "Volatile EE": {
        "de": "Volatile EE (Wind, Wasser, PV)",
        "en": "Volatile RES (Wind, Hydro, PV)",
        "color": "green"
    },
    "Erzeugung": {
        "de": "Erzeugung",
        "en": "Production",
        "color": "green"
    },
}

# Debuggung

if VERBOSE:
    print(__name__, " loaded!")
