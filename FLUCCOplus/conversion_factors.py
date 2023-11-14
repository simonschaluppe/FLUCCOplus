# Daten aus (Stolz & Frischknecht, 2017, s.5)
#s = "AtomkraftwerkMJ4.21 0.06 4.14 0.01 - 0.006 0.005 125.8 Erdgaskombikraftwerk GuDMJ2.22 2.21 0.01 0.01 - 0.129 0.121 85.6 Braunkohlekraftwerk (Dampf)MJ3.95 3.90 0.03 0.01 - 0.377 0.370 220.2 Steinkohlekraftwerk (Dampf)MJ3.94 3.87 0.04 0.03 - 0.344 0.298 213.4 Kraftwerk SchwerölMJ3.83 3.78 0.04 0.01 - 0.281 0.268 302.5 KehrichtverbrennungMJ0.02 0.01 0.00 0.00 1.11 0.002 0.001 8.9 Heizkraftwerk HolzMJ3.88 0.19 0.05 3.64 - 0.033 0.012 81.9 Blockheizkraftwerk DieselMJ3.28 3.23 0.04 0.01 - 0.229 0.215 187.9 Blockheizkraftwerk GasMJ2.94 2.92 0.01 0.01 - 0.186 0.159 122.3 Blockheizkraftwerk BiogasMJ0.91 0.50 0.32 0.09 1.11 0.112 0.032 103.8 Blockheizkraftwerk Biogas, LandwirtschaftMJ0.19 0.09 0.06 0.04 1.11 0.049 0.006 63.8 FotovoltaikMJ1.56 0.28 0.05 1.22 - 0.027 0.022 48.4 Fotovoltaik SchrägdachMJ1.54 0.27 0.05 1.22 - 0.025 0.021 46.9 Fotovoltaik FlachdachMJ1.55 0.28 0.04 1.22 - 0.027 0.022 43.2 Fotovoltaik FassadeMJ1.70 0.39 0.07 1.24 - 0.037 0.032 62.6 WindkraftMJ1.29 0.08 0.01 1.20 - 0.007 0.006 20.5 WasserkraftMJ1.20 0.02 0.01 1.17 - 0.003 0.002 12.2 PumpspeicherungMJ3.90 0.46 2.81 0.63 - 0.039 0.034 125.3 Heizkraftwerk GeothermieMJ3.36 0.16 0.03 3.17 - 0.009 0.008 28.6 CH-ProduktionsmixMJ2.50 0.07 1.78 0.66 - 0.007 0.005 63.5 Mix zertifizierte Stromprodukte CHMJ1.21 0.03 0.01 1.17 0.01 0.004 0.003 13.3 CH-VerbrauchermixMJ3.00 0.35 2.17 0.49 0.02 0.028 0.025 96.4 ENTSO-E-MixMJ3.18 1.80 1.09 0.30 - 0.146 0.136 152.2"
# db = [i.split(" ") for i in s.split("MJ")]
# new = []
# for r, row in enumerate(db):
#     new.append(list())
#     for i, item in enumerate(row):
#         try:
#             f = float(item)
#             new[r - 1].append(f)
#         except ValueError:
#             if item == "-":
#                 new[r - 1].append(0.)
#             else:
#                 new[r].append(item)
# new2 = list()
# for row in new:
#     l = len(row)
#     h = " ".join(row[0:-8])
#     new2.append([h, *row[-8:]])
# new2 = new2[:-1]
# header = """Primärenergiefaktor total [MJ-eq]
# Primärenergiefaktor fossil [MJ-eq]
# Primärenergiefaktor nuklear  [MJ-eq]
# Primärenergiefaktor total erneuerbar [MJ-eq]
# Primärenergiefaktor Abwärme / Abfall [MJ-eq]
# CO2-Äquivalente  [kg CO2-eq]
# Kohlendioxid, fossil [kg CO2-eq]
# Umweltbelastungspunkte [UBP'13]"""
# header = header.split("\n")
# faktoren = {r[0]: {h: v for h, v in zip(header, r[1:])} for r in new2}


# above code produces the following dict

CONVERSION_FACTORS = {'Atomkraftwerk': {'Primärenergiefaktor total [MJ-eq]': 4.21,
  'Primärenergiefaktor fossil [MJ-eq]': 0.06,
  'Primärenergiefaktor nuklear  [MJ-eq]': 4.14,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.006,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.005,
  "Umweltbelastungspunkte [UBP'13]": 125.8},
 'Erdgaskombikraftwerk GuD': {'Primärenergiefaktor total [MJ-eq]': 2.22,
  'Primärenergiefaktor fossil [MJ-eq]': 2.21,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.01,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.129,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.121,
  "Umweltbelastungspunkte [UBP'13]": 85.6},
 'Braunkohlekraftwerk (Dampf)': {'Primärenergiefaktor total [MJ-eq]': 3.95,
  'Primärenergiefaktor fossil [MJ-eq]': 3.9,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.03,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.377,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.37,
  "Umweltbelastungspunkte [UBP'13]": 220.2},
 'Steinkohlekraftwerk (Dampf)': {'Primärenergiefaktor total [MJ-eq]': 3.94,
  'Primärenergiefaktor fossil [MJ-eq]': 3.87,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.04,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.03,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.344,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.298,
  "Umweltbelastungspunkte [UBP'13]": 213.4},
 'Kraftwerk Schweröl': {'Primärenergiefaktor total [MJ-eq]': 3.83,
  'Primärenergiefaktor fossil [MJ-eq]': 3.78,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.04,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.281,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.268,
  "Umweltbelastungspunkte [UBP'13]": 302.5},
 'Kehrichtverbrennung': {'Primärenergiefaktor total [MJ-eq]': 0.02,
  'Primärenergiefaktor fossil [MJ-eq]': 0.01,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.0,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.0,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 1.11,
  'CO2-Äquivalente  [kg CO2-eq]': 0.002,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.001,
  "Umweltbelastungspunkte [UBP'13]": 8.9},
 'Heizkraftwerk Holz': {'Primärenergiefaktor total [MJ-eq]': 3.88,
  'Primärenergiefaktor fossil [MJ-eq]': 0.19,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.05,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 3.64,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.033,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.012,
  "Umweltbelastungspunkte [UBP'13]": 81.9},
 'Blockheizkraftwerk Diesel': {'Primärenergiefaktor total [MJ-eq]': 3.28,
  'Primärenergiefaktor fossil [MJ-eq]': 3.23,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.04,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.229,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.215,
  "Umweltbelastungspunkte [UBP'13]": 187.9},
 'Blockheizkraftwerk Gas': {'Primärenergiefaktor total [MJ-eq]': 2.94,
  'Primärenergiefaktor fossil [MJ-eq]': 2.92,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.01,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.01,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.186,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.159,
  "Umweltbelastungspunkte [UBP'13]": 122.3},
 'Blockheizkraftwerk Biogas': {'Primärenergiefaktor total [MJ-eq]': 0.91,
  'Primärenergiefaktor fossil [MJ-eq]': 0.5,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.32,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.09,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 1.11,
  'CO2-Äquivalente  [kg CO2-eq]': 0.112,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.032,
  "Umweltbelastungspunkte [UBP'13]": 103.8},
 'Blockheizkraftwerk Biogas, Landwirtschaft': {'Primärenergiefaktor total [MJ-eq]': 0.19,
  'Primärenergiefaktor fossil [MJ-eq]': 0.09,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.06,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.04,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 1.11,
  'CO2-Äquivalente  [kg CO2-eq]': 0.049,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.006,
  "Umweltbelastungspunkte [UBP'13]": 63.8},
 'Fotovoltaik': {'Primärenergiefaktor total [MJ-eq]': 1.56,
  'Primärenergiefaktor fossil [MJ-eq]': 0.28,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.05,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.22,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.027,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.022,
  "Umweltbelastungspunkte [UBP'13]": 48.4},
 'Fotovoltaik Schrägdach': {'Primärenergiefaktor total [MJ-eq]': 1.54,
  'Primärenergiefaktor fossil [MJ-eq]': 0.27,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.05,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.22,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.025,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.021,
  "Umweltbelastungspunkte [UBP'13]": 46.9},
 'Fotovoltaik Flachdach': {'Primärenergiefaktor total [MJ-eq]': 1.55,
  'Primärenergiefaktor fossil [MJ-eq]': 0.28,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.04,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.22,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.027,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.022,
  "Umweltbelastungspunkte [UBP'13]": 43.2},
 'Fotovoltaik Fassade': {'Primärenergiefaktor total [MJ-eq]': 1.7,
  'Primärenergiefaktor fossil [MJ-eq]': 0.39,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.07,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.24,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.037,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.032,
  "Umweltbelastungspunkte [UBP'13]": 62.6},
 'Windkraft': {'Primärenergiefaktor total [MJ-eq]': 1.29,
  'Primärenergiefaktor fossil [MJ-eq]': 0.08,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.01,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.2,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.007,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.006,
  "Umweltbelastungspunkte [UBP'13]": 20.5},
 'Wasserkraft': {'Primärenergiefaktor total [MJ-eq]': 1.2,
  'Primärenergiefaktor fossil [MJ-eq]': 0.02,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.01,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.17,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.003,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.002,
  "Umweltbelastungspunkte [UBP'13]": 12.2},
 'Pumpspeicherung': {'Primärenergiefaktor total [MJ-eq]': 3.9,
  'Primärenergiefaktor fossil [MJ-eq]': 0.46,
  'Primärenergiefaktor nuklear  [MJ-eq]': 2.81,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.63,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.039,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.034,
  "Umweltbelastungspunkte [UBP'13]": 125.3},
 'Heizkraftwerk Geothermie': {'Primärenergiefaktor total [MJ-eq]': 3.36,
  'Primärenergiefaktor fossil [MJ-eq]': 0.16,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.03,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 3.17,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.009,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.008,
  "Umweltbelastungspunkte [UBP'13]": 28.6},
 'CH-Produktionsmix': {'Primärenergiefaktor total [MJ-eq]': 2.5,
  'Primärenergiefaktor fossil [MJ-eq]': 0.07,
  'Primärenergiefaktor nuklear  [MJ-eq]': 1.78,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.66,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.007,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.005,
  "Umweltbelastungspunkte [UBP'13]": 63.5},
 'Mix zertifizierte Stromprodukte CH': {'Primärenergiefaktor total [MJ-eq]': 1.21,
  'Primärenergiefaktor fossil [MJ-eq]': 0.03,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.01,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 1.17,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.01,
  'CO2-Äquivalente  [kg CO2-eq]': 0.004,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.003,
  "Umweltbelastungspunkte [UBP'13]": 13.3},
 'CH-Verbrauchermix': {'Primärenergiefaktor total [MJ-eq]': 3.0,
  'Primärenergiefaktor fossil [MJ-eq]': 0.35,
  'Primärenergiefaktor nuklear  [MJ-eq]': 2.17,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.49,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.02,
  'CO2-Äquivalente  [kg CO2-eq]': 0.028,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.025,
  "Umweltbelastungspunkte [UBP'13]": 96.4},
 'ENTSO-E-Mix': {'Primärenergiefaktor total [MJ-eq]': 3.18,
  'Primärenergiefaktor fossil [MJ-eq]': 1.8,
  'Primärenergiefaktor nuklear  [MJ-eq]': 1.09,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.3,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.146,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.136,
  "Umweltbelastungspunkte [UBP'13]": 152.2},
  'OIB RL-E 19 Liefermix': {'Primärenergiefaktor total [MJ-eq]': 1.62,
  'Primärenergiefaktor fossil [MJ-eq]': 1.02,
  'Primärenergiefaktor nuklear  [MJ-eq]': 0.0,
  'Primärenergiefaktor total erneuerbar [MJ-eq]': 0.61,
  'Primärenergiefaktor Abwärme / Abfall [MJ-eq]': 0.0,
  'CO2-Äquivalente  [kg CO2-eq]': 0.227,
  'Kohlendioxid, fossil [kg CO2-eq]': 0.227,
  "Umweltbelastungspunkte [UBP'13]": 0}}


conversion_mapping = {
    "biomass": "Heizkraftwerk Holz",
    "hydro": "Wasserkraft",
    "solar": "Fotovoltaik",
    "wind": "Windkraft",
    "geothermal": "Heizkraftwerk Geothermie",
    "coal": "Braunkohlekraftwerk (Dampf)",
    "gas": "Erdgaskombikraftwerk GuD",
    "nuclear": "Atomkraftwerk",
    "oil": "Blockheizkraftwerk Diesel",
    "unknown": "ENTSO-E-Mix",
    "battery_discharge": "ENTSO-E-Mix",
    "hydro_discharge": "OIB RL-E 19 Liefermix"
}

conversion_columns = [
    "Primärenergiefaktor total [MJ-eq]",
    "Primärenergiefaktor fossil [MJ-eq]",
    "Primärenergiefaktor nuklear  [MJ-eq]",
    "Primärenergiefaktor total erneuerbar [MJ-eq]",
    "Primärenergiefaktor Abwärme / Abfall [MJ-eq]",
    "CO2-Äquivalente  [kg CO2-eq]",
    ]

PE_factors_OIB2019 = {
    'biomass':
        {"fPE":         1.13,
         "fPE,n.ern.":  0.1,
         "fPE,ern.":    1.03},
    'hydro':
        {"fPE":         1.,
         "fPE,n.ern.":  0,
         "fPE,ern.":    1.0},
    'solar':
        {"fPE":         1.,
         "fPE,n.ern.":  0,
         "fPE,ern.":    1.0},
    'wind':
        {"fPE":         1.,
         "fPE,n.ern.":  0,
         "fPE,ern.":    1.0},
    'geothermal':
        {"fPE":         1.,
         "fPE,n.ern.":  0,
         "fPE,ern.":    1.0},
    'coal':
        {"fPE":         1.46,
         "fPE,n.ern.":  1.46,
         "fPE,ern.":    0.0},
    'gas':
        {"fPE":         1.1,
         "fPE,n.ern.":  1.1,
         "fPE,ern.":    0.0},
    'nuclear':
        {"fPE":         1.63,
         "fPE,n.ern.":  0.28,
         "fPE,ern.":    1.32},
    'oil':
        {"fPE":         1.2,
         "fPE,n.ern.":  1.2,
         "fPE,ern.":    0.0},
    'unknown':
        {"fPE":         1.63,
         "fPE,n.ern.":  0.28,
         "fPE,ern.":    1.32},
    'battery_discharge':
        {"fPE":         1.63,
         "fPE,n.ern.":  0.28,
         "fPE,ern.":    1.32},
    'hydro_discharge':
        {"fPE":         1.63,
         "fPE,n.ern.":  0.28,
         "fPE,ern.":    1.32},
}

def add_PE(df):
    """
    calc PE factors for energy carriers
    :param df:
    :return:
    """
    pass

