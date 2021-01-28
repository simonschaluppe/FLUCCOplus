from FLUCCOplus.utils import logg
from FLUCCOplus.notebooks import *

from matplotlib.figure import Figure

from dataclasses import dataclass, field, fields
@dataclass()
class Variable:
    name:str
    ylabel:str
    agg:object
    ylabel_agg:str





@log
def average(df, vars):
    fig = Figure(figsize=(15, 15))
    ax = fig.subplots(len(vars), 3)
    for col, var in enumerate(vars):
        sns.lineplot(x=df.index.hour, y=var.name, data=df, hue=df.index.year, ax=ax[col][0])
        sns.lineplot(x=df.index.month, y=var.name, data=df, hue=df.index.year, ax=ax[col][1])
        # df.groupby(df.index.year)[var.name].agg(var.agg).plot(kind="bar", rot=0, ax=ax[col][2])
        sns.barplot(x=df.index.year.unique(), y=var.name, data=df.groupby(df.index.year).agg(var.agg), ax=ax[col][2])
        ax[col][0].set(xlabel="Durchschnittliche Stunde", ylabel=var.ylabel)
        ax[col][1].set(xlabel="Monatsmittel", ylabel=var.ylabel)
        ax[col][2].set(xlabel="Jahr", ylabel=var.ylabel_agg)
    return fig

def average_sources(df, var, ax):

    fig = Figure(figsize=(15, 15))
    ax = fig.subplots(1, 3)
    df.groupby(df.index.month)[var.name].agg(var.agg).plot(kind="bar",stacked=True, ax=ax[2])
    # df.groupby(df.index.year)[var.name].agg(var.agg).plot(kind="bar", rot=0, ax=ax[col][2])
    sns.barplot(x=df.index.year.unique(), y=var.name, data=df.groupby(df.index.year).agg(var.agg), ax=ax[2])
    ax[0].set(xlabel="Durchschnittliche Stunde", ylabel=var.ylabel)
    ax[1].set(xlabel="Monatsmittel", ylabel=var.ylabel)
    ax[2].set(xlabel="Jahr", ylabel=var.ylabel_agg)



@logg
def plot_41_ec_eb(df, carriers, uses, year):

    # %%
    return df