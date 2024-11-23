import pandas as pd

size = 8760  #Tag, Woche, 2WO, 4WO
timeframes = [24, 24*7, 24*7*2, 24*7*4]
excel_pfad = "C:/Users/Simon Schneider/Downloads/FragenReihung.xlsx" 
sheet_name = "python" # nur die daten, muss "cost" als header beinhalten
excel_output = "Out.xlsx"


df = pd.read_excel(excel_pfad, sheet_name="python")
for timeframe in timeframes:
    # Create a column with the cycle ID (e.g., each day as a separate group)
    df[f"cycle {timeframe}"] = df.index % timeframe
    df[f"group {timeframe}"] = df.index // timeframe
    df[f"timeframe {timeframe}h ordering"] = (
        df.groupby(f"group {timeframe}")["cost"]
        .rank(method="first", ascending=False)
        .astype(int)  # Shift to zero-based index if needed
    )
    
df.to_excel(excel_output, sheet_name="python")
df
