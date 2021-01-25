#%% md

# AP4 FLUCCOplus

## TASK 4.1
### Vergleich E-Control
# [asdasd](notebooks/4.1-1-Econtrol_Validation.ipynb)
#%%
import electricitymap
import econtrol

ECONTROL_PATH = ""
df_ec = econtrol.parse_econtrol(path=ECONTROL_PATH)
(df_ec
 .pipe(econtrol.clean_colnames)
 )

EM_PATH =""
df_em = electricitymap.parse(path=EM_PATH, year:int)

df_em_sum = (df_em

       .groupby)
#%% md

### CO2 Emissionen
#### Vergleich zu OIB RL 6

#
# [asdasd](notebook.ipynb)

#%%

#%% md
## TASK 4.2

### Szenarien Überblick

#%%




#%% md

## TASK 4.3

#%%



#%%



