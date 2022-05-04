from FLUCCOplus.utils import *
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

def average_sources(df, var):

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

def emissionyear(rs, oib_co2, fig, ax, var="carbon_intensity_avg",year=2015):
    # em co2 corriduor
    sns.lineplot(x=rs.index.week, y=var, data=rs, color="black", ax=ax, ci=99.9)
    # em yearly
    co2_mean_em = rs.loc[rs.index.year==year, var].mean()
    pd.Series([co2_mean_em for m in rs.index.month], rs.index.isocalendar().week).plot(ax=ax, color="black", linewidth = 3)
    # em all years average
    pd.Series([234.42 for m in rs.index.month], rs.index.isocalendar().week).plot(ax=ax, color="black",
                                                                                       linewidth=2)
    # oib 18 monthly
    oib18 = pd.Series([oib_co2.loc[m-1] for m in rs.index.month], rs.index.isocalendar().week)
    oib18[3:-3].plot(color="red", linewidth=2, ax=ax) #indexin weirdness (3:-3)
    # oib 19 yearly
    oib19 = pd.Series([227 for m in rs.index.month], rs.index.isocalendar().week)
    oib19.plot(color="darkred", linewidth=3, ax=ax)


def plot_OIBCO2_comparison(rs, oib, years=[2015,2016,2017,2018,2019]):
    fig, ax = plt.subplots(1, len(years), figsize=(4*len(years),5), sharey=True)
    for i, y in enumerate(years):
        emissionyear(rs.loc[rs.index.year == y], oib_co2=oib, fig=fig, ax=ax[i], year=y)
        ax[i].set_xticklabels([])
        ax[i].set_xticks(np.linspace(0,54,7))
        ax[i].set_xlim(0,54)
        ax[i].set_ylim(50,400)
        ax[i].set_xlabel(str(y), size=12)

    ax[0].set_ylabel('CO$_2$-Intensität [g/kWh$_e$$_l$]')
    ax[0].legend(["Measurement data (EM)", "annual average (EM)", "2015-2018 average (EM)","OIB Rl6 Monthly (2018)","OIB RL6 2019"], loc='lower left', fontsize=12)
    fig.tight_layout()
    return fig

def plot_HDW(df,
             var="carbon_intensity_avg",
             ylabel="Carbon emissions [g$_{CO2eq}$/kWh]",
             xlabel="",
             colors=["darkgrey", "black", "black"],
             legend=["Hourly","Daily average", "Weekly average"],
             xlim=("2019-01-01", "2019-12-31"),
             figsize=(10,8),
             fig=None,
             ax=None):
    """
    Plots the hourly, daily average and weekly average of a given df variable
    """

    df_daily = df.resample("D").mean()
    df_weekly = df.resample("W").mean()
    # df_monthly = df.resample("M").mean()
    if fig == None or ax == None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)

    df[var].plot(ax=ax, color=colors[0], marker='.', alpha=0.3, linestyle='None', legend=False)
    ax.set_xlabel(xlabel)

    df_daily[var].plot(ax=ax, color=colors[1], alpha=0.8, legend=False)
    ax.set_xlabel(xlabel)

    df_weekly[var].plot(color=colors[2], linewidth=1.5, ax=ax, legend=False)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    ax.set_xlim(xlim[0], xlim[1])
    ax.legend(legend, loc='lower left', fontsize=12)
    fig.tight_layout()
    return fig

#def plot_comp_residuallast(df, df2):
 #   for i, col in enumerate(df13_sign.columns):
  #      vis = pd.pivot_table(df13_sign, index=df13_sign.index.date, columns=df13_sign.index.hour, values=col)
   #     sns.heatmap(vis.T, cbar=False, yticklabels=False, ax=ax[i])
    #    ax[i].set_title(col, loc="right", color="lime", fontsize=10, pad=-14)
     #   months = MonthLocator()
      #  monthsFmt = DateFormatter("%b")
       # ax[i].xaxis.set_major_locator(months)
        #ax[i].xaxis.set_major_formatter(monthsFmt)



def plot_comp(df, df2,
                 ylabel="Energie [kWh]",
                 xlabel="Zeit [Stunden]",
                 figsize=(15,6),
                 fig=None, ax=None, start=0, stop=8760, legend1=False, legend2=False):
    xh = np.arange(0, 8760, 1)

    if fig == None or ax == None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        plt.plot(xh[start:stop], df[start:stop], "b", label=legend1)
        plt.plot(xh[start:stop], df2[start:stop], "g", label=legend2)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend()
    return fig, ax

def plot_monthly_comp(df, df2,
                 ylabel="Energie [kWh]",
                 xlabel="Zeit [Monate]",
                 figsize=(15,6),
                 fig=None, ax=None, start=0, stop=12, legend1=False, legend2=False):
    xh = np.arange(1, 13, 1)

    if fig == None or ax == None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        plt.plot(xh[start:stop], df.resample("M").sum()[start:stop], label=legend1)
        plt.plot(xh[start:stop], df2.resample("M").sum()[start:stop], label=legend2)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(xh)
    ax.ticklabel_format(axis='both', style='plain')
    ax.legend(loc='upper right')
    return fig, ax

def plot_monthly(df,
                 ylabel="Energie [kWh]",
                 xlabel="Zeit [Monate]",
                 figsize=(15,6),
                 fig=None, ax=None, start=0, stop=12):

    xh = np.arange(1, 13, 1)
    colName = ['Photovoltaik', 'Windkraft', 'Pumpspeicher', 'Laufkraft', 'Strombedarf']
    colors = {colName[0]: 'orange', colName[1]: 'cian', colName[2]: 'forestgreen',
              colName[3]: 'darkgreen', colName[4]: 'gray'}
    if fig == None or ax == None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        plt.plot(xh[start:stop], df.resample("M").sum()[start:stop])
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(xh)
    ax.ticklabel_format(axis='both', style='plain')
    ax.legend(loc='upper right')
    return fig, ax

def plot_analyse_PVfirst(df,
                 summerweek_start,
                 summerweek_stop,
                 winterweek_start,
                 winterweek_stop,
                 ylabel="Energie [kWh]",
                 xlabel="Zeit [Monate]",
                figsize=(18, 11)):

    df_summer = df.loc[summerweek_start:summerweek_stop]
    df_winter = df.loc[winterweek_start:winterweek_stop]

    max_score_wind = max((df_summer["RES"].max()), (df_winter["RES"].max()), (df_summer["Strombedarf"].max()), (df_winter["Strombedarf"].max()))
    ax_scale_wind = 0, (max_score_wind + 1000)
    ax_scale_wind2 = ((min((df_summer["Residual_ohne_Wind"].min()), (df_winter["Residual_ohne_Wind"].min()))) - 1000), (
                (max((df_summer["Residual_ohne_Wind"].max()), (df_winter["Residual_ohne_Wind"].max()))) + 1000)

    fig, ax = plt.subplots(3, 2, figsize=figsize)

    df_summer["Strombedarf"].plot(ax=ax[0, 0]).set(title="Sommerwoche Wind", xlabel=xlabel,
                                                   ylabel=ylabel, ylim=ax_scale_wind)
    fill1 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"], color="forestgreen")
    fill2 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"]+df_summer["PVDV"], df_summer["Non_volatiles"], color='orange')
    fill3 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"]+df_summer["PVDV"], df_summer["Non_volatiles"]+df_summer["PVDV"]+df_summer["WindkraftDV"], color="c")
    fill4 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"]+df_summer["PVDV"]+df_summer["WindkraftDV"], df_summer["Non_volatiles"]+df_summer["PVDV"]+df_summer["WindkraftDV"]+df_summer["PVUeSch"], color="y")
    fill5 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"]+df_summer["PVDV"]+df_summer["WindkraftDV"]+df_summer["PVUeSch"] + df_summer["WindkraftUeSch"], df_summer["Non_volatiles"]+df_summer["PVDV"]+df_summer["WindkraftDV"]+df_summer["PVUeSch"], color='blue')

    df_winter["Strombedarf"].plot(ax=ax[0, 1]).set(title="Winterwoche Wind", xlabel=xlabel,
                                                   ylabel=ylabel, ylim=ax_scale_wind)
    fill6 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"], color="forestgreen")
    fill7 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"]+df_winter["PVDV"], df_winter["Non_volatiles"], color='orange')
    fill8 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"]+df_winter["PVDV"],df_winter["Non_volatiles"]+df_winter["PVDV"]+df_winter["WindkraftDV"], color="c")
    fill9 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"]+df_winter["PVDV"]+df_winter["WindkraftDV"],df_winter["Non_volatiles"] + df_winter["PVDV"]+df_winter["WindkraftDV"]+df_winter["PVUeSch"], color="y")
    fill10 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"]+df_winter["PVDV"]+df_winter["WindkraftDV"]+df_winter["PVUeSch"] + df_winter["WindkraftUeSch"], df_winter["Non_volatiles"]+df_winter["PVDV"]+df_winter["WindkraftDV"]+df_winter["PVUeSch"], color="blue")
    ax[0, 0].legend([fill5, fill4, fill3, fill2, fill1],
                    ["Windkraft Überschuss", "PV Überschuss", "Windkraft Direktverbrauch", "PV Direktverbrauch",
                     "Nicht volatile Energieträger Direktverbrauch"], loc="lower left")
    ax[0, 1].legend([fill10, fill9, fill8, fill7, fill6],
                    ["Windkraft Überschuss", "PV Überschuss", "Windkraft Direktverbrauch", "PV Direktverbrauch",
                     "Nicht volatile Energieträger Direktverbrauch"], loc="lower left")

    df_summer[["Wind_useful", "Windkraft", "Residual_ohne_Wind", "Wind_Nennleistung"]].plot(ax=ax[1, 0]).set(
        xlabel="Datum", ylabel="Energie [GWh]", ylim=ax_scale_wind2)
    fill11 = ax[1, 0].fill_between(df_summer.index, df_summer["Zero"], df_summer["Wind_useful"], color='c')
    fill12 = ax[1, 0].fill_between(df_summer.index, df_summer["Wind_useful"], df_summer["Windkraft"], color='blue')
    df_winter[["Wind_useful", "Windkraft", "Residual_ohne_Wind", "Wind_Nennleistung"]].plot(ax=ax[1, 1]).set(
        xlabel="Datum", ylabel="Energie [GWh]", ylim=ax_scale_wind2)
    fill13 = ax[1, 1].fill_between(df_winter.index, df_winter["Zero"], df_winter["Wind_useful"], color='c')
    fill14 = ax[1, 1].fill_between(df_winter.index, df_winter["Wind_useful"], df_winter["Windkraft"], color='blue')

    df_windrel_summer = df_summer.Wind_rel.where(df_summer.Windkraft > df_summer.Wind_useful)
    df_windrel_summer.plot(ax=ax[2, 0]).set(xlabel="Datum", ylabel="Windkraft Überschuss zur installierten Leistung",
                                            ylim=(0, 1))
    df_windrel_winter = df_winter.Wind_rel.where(df_winter.Windkraft > df_winter.Wind_useful)
    df_windrel_winter.plot(ax=ax[2, 1]).set(xlabel="Datum", ylabel="Windkraft Überschuss zur installierten Leistung",
                                            ylim=(0, 1))
    return fig, ax

def plot_analyse_WINDfirst(df,
                 summerweek_start,
                 summerweek_stop,
                 winterweek_start,
                 winterweek_stop,
                 ylabel="Energie [kWh]",
                 xlabel="Zeit [Monate]",
                figsize=(18, 11)):

    df_summer = df.loc[summerweek_start:summerweek_stop]
    df_winter = df.loc[winterweek_start:winterweek_stop]

    max_score_wind = max((df_summer["RES"].max()), (df_winter["RES"].max()))
    ax_scale_wind = 0, (max_score_wind + 1000)
    ax_scale_wind2 = ((min((df_summer["Residual_ohne_Wind"].min()), (df_winter["Residual_ohne_Wind"].min()))) - 1000), (
                (max((df_summer["Residual_ohne_Wind"].max()), (df_winter["Residual_ohne_Wind"].max()))) + 1000)

    fig, ax = plt.subplots(3, 2, figsize=figsize)

    df_summer["Strombedarf"].plot(ax=ax[0, 0]).set(title="Sommerwoche Wind", xlabel=xlabel,
                                                   ylabel=ylabel, ylim=ax_scale_wind)
    fill1 = ax[0, 0].fill_between(df_summer.index, df_summer["Non_volatiles"], color="forestgreen")
    fill2 = ax[0, 0].fill_between(df_summer.index, df_summer["WindkraftDV"]+df_summer["Non_volatiles"], df_summer["Non_volatiles"], color='c')
    fill3 = ax[0, 0].fill_between(df_summer.index, df_summer["WindkraftDV"]+df_summer["Non_volatiles"] + df_summer["PVDV"], df_summer["WindkraftDV"]+df_summer["Non_volatiles"] + df_summer["PVDV"]+df_summer["WindkraftUeSch"], color="blue")
    fill4 = ax[0, 0].fill_between(df_summer.index, df_summer["WindkraftDV"]+df_summer["Non_volatiles"] + df_summer["PVDV"], df_summer["WindkraftDV"]+df_summer["Non_volatiles"], color="y")
    fill5 = ax[0, 0].fill_between(df_summer.index, df_summer["RES"]-df_summer["PVUeSch"], df_summer["RES"], color='orange')

    df_winter["Strombedarf"].plot(ax=ax[0, 1]).set(title="Winterwoche Wind", xlabel=xlabel,
                                                   ylabel=ylabel, ylim=ax_scale_wind)
    fill6 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"], color="forestgreen")
    fill7 = ax[0, 1].fill_between(df_winter.index, df_winter["WindkraftDV"]+df_winter["Non_volatiles"], df_winter["Non_volatiles"], color='c')
    fill8 = ax[0, 1].fill_between(df_winter.index, df_winter["WindkraftDV"]+df_winter["Non_volatiles"] + df_winter["PVDV"], df_winter["WindkraftDV"]+df_winter["Non_volatiles"] + df_winter["PVDV"]+df_winter["WindkraftUeSch"], color="blue")
    fill9 = ax[0, 1].fill_between(df_winter.index, df_winter["Non_volatiles"]+df_winter["WindkraftDV"] + df_winter["PVDV"], df_winter["WindkraftDV"]+df_winter["Non_volatiles"], color="y")
    fill10 = ax[0, 1].fill_between(df_winter.index, df_winter["RES"]-df_winter["PVUeSch"], df_winter["RES"], color='orange')
    ax[0, 0].legend([fill5, fill4, fill3, fill2, fill1],
                    ["PV Überschuss", "PV Direktverbrauch", "Windkraft Überschuss", "Wind Direktverbrauch",
                     "Nicht volatile Energieträger Direktverbrauch"], loc="lower left")
    ax[0, 1].legend([fill10, fill9, fill8, fill7, fill6],
                    ["PV Überschuss", "PV Direktverbrauch", "Windkraft Überschuss", "Wind Direktverbrauch",
                     "Nicht volatile Energieträger Direktverbrauch"], loc="lower left")

    df_summer[["Wind_useful", "Windkraft", "Residual_ohne_Wind", "Wind_Nennleistung"]].plot(ax=ax[1, 0]).set(
        xlabel="Datum", ylabel="Energie [GWh]", ylim=ax_scale_wind2)
    fill11 = ax[1, 0].fill_between(df_summer.index, df_summer["Zero"], df_summer["Windkraft"]-df_summer["WindkraftUeSch"], color='c')
    fill12 = ax[1, 0].fill_between(df_summer.index, df_summer["Wind_useful"], df_summer["Windkraft"], where=df_summer["WindkraftUeSch"]>0, color='blue')
    df_winter[["Wind_useful", "Windkraft", "Residual_ohne_Wind", "Wind_Nennleistung"]].plot(ax=ax[1, 1]).set(
        xlabel="Datum", ylabel="Energie [GWh]", ylim=ax_scale_wind2)
    fill13 = ax[1, 1].fill_between(df_winter.index, df_winter["Zero"], df_winter["Windkraft"]-df_winter["WindkraftUeSch"], color='c')
    fill14 = ax[1, 1].fill_between(df_winter.index, df_winter["Wind_useful"], df_winter["Windkraft"], where=df_winter["WindkraftUeSch"]>0, color='blue')

    df_windrel_summer = df_summer.Wind_rel.where(df_summer.Windkraft > df_summer.Wind_useful)
    df_windrel_summer.plot(ax=ax[2, 0]).set(xlabel="Datum", ylabel="Windkraft Überschuss zur installierten Leistung",
                                            ylim=(0, 1))
    df_windrel_winter = df_winter.Wind_rel.where(df_winter.Windkraft > df_winter.Wind_useful)
    df_windrel_winter.plot(ax=ax[2, 1]).set(xlabel="Datum", ylabel="Windkraft Überschuss zur installierten Leistung",
                                            ylim=(0, 1))
    return fig, ax