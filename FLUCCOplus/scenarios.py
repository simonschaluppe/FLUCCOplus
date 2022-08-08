import pandas as pd

import FLUCCOplus.config as config
import FLUCCOplus.transform as traffo
import FLUCCOplus.plots as fpp
import FLUCCOplus.signals as fps
import matplotlib.pyplot as plt
#import utils
from FLUCCOplus.utils import *

from enum import Enum

class Names:
    electricity_map_2020 = "EM2018"
    electricity_map_2019 = "EM2019"
    econtrol_2019 = "E-Control 2019"
    veigl17_2030 = "Energie und Klimazukunft 2030 (Veigl17)"
    veigl17_2050 = "Energie und Klimazukunft 2050 (Veigl17)"
    uba16_2030 = "Erneuerbare Energie 2030 (UBA16)"
    uba16_2050 = "Erneuerbare Energie 2050 (UBA16)"
    uba17_2030_WEM = "WEM 2030 (UBA17)"
    uba17_2030_WAM = "Transition 2030 (UBA17)"
    uba17_2050_WEM = "WEM 2050 (UBA17)"
    uba17_2050_WAM = "Transition 2050 (UBA17)"
    #name = "100% Erneuerbare Deckung 2050 (FLUCCO+)"
    flucco_2050 = "100% Erneuerbare Deckung 2050 inkl Methan (FLUCCO+)"
    flucco_2050_vol = "100% Erneuerbare Deckung 2050 ohne Speicherausbau (FLUCCO+)"


@log
def read(path):
    from FLUCCOplus.config import DATA_RAW
    return pd.read_excel(DATA_RAW / "szenarien"/ path,
                  sheet_name="scenarios",
                  index_col=0, skiprows=range(1, 3))

@logg
def start_pipeline(df):
    return df.copy()

@logg
def rename_cols_to_common(df):
    df = df.rename(columns=EM_TO_EXCEL_colnames)
    return df



@logg
def convert_PJ_to_GWH(df):
    jahr = df["Jahr"]
    df = df.drop("Jahr", axis=1)
    df = df * PJ_TO_GWH
    df.insert(0,"Jahr", jahr)
    df.index.rename("Szenario", inplace=True)
    return df

@logg
def NaNtoZero(df):
    return df.fillna(0)

@logg
def format_df(df):
    return df.astype({"Jahr":"int32"})


@logg
def get_scenario(scenario_name, col_dict, Excel_to_EM_dict):
    """gets the preprocessed scenario including residual loads"""
    df_scenario = pd.DataFrame()

    for col in Excel_to_EM_dict.keys():
        # %%
        c = col_dict[col]
        df_scenario[col] = c[scenario_name]

    df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] = df_scenario["Strombedarf"] - df_scenario["Volatile EE"]
    df_scenario["RES1 (RES0-Pumpspeicher)"] = df_scenario["RES0 (Bedarf-PV,Wind,Laufkraft)"] - df_scenario[
        "Pumpspeicher"]
    df_scenario["RES2 (RES1-Nicht-Volatile)"] = df_scenario["RES1 (RES0-Pumpspeicher)"] - df_scenario["Nicht-Volatile"]

    # df_sc["RES0"][scenario_name] = df_scenario["RES0"]
    return df_scenario



def all():
    """
    Returns all W2S Scenarios in [GWh/a]
    :return:
    """
    sc = (read("szenarien_w2s.xlsx")
          .pipe(start_pipeline)
          .pipe(NaNtoZero)
          .pipe(format_df)
          .pipe(convert_PJ_to_GWH)
          )
    return sc


@log
def factors(source, target, scenarios):
    """

    :param source: String or Index int of source scenario
    :param target: String or Index int of target scenario
    :param scenarios: Dataframe with Scenarios, must include all EM_TO_EXCEL_colnames
    :return: dict with factors for all EM_TO_EXCEL_colnames
    """
    if type(source) == int:
        src = scenarios.index[source]
    else: src = source

    if type(target) == int:
        tgt = scenarios.index[target]
    else: tgt = target

    carriers = EM_TO_EXCEL_colnames.values()
    f = scenarios.loc[tgt, carriers] / scenarios.loc[src, carriers]
    factors = {"source": src, "target": tgt}
    factors.update({i: j for i, j in zip(carriers, f)})

    return factors

#class Comparison:
 #   def __init__(self, scenario1, scenario2):


class Scenario:
    "represents an Electricity SCenario with variable scaling of energy carrieres and demands, and transformations "

    def __init__(self, name, scenario, em_base=None, transformation_scenario=None):
        self.name = name
        scenarios = all()
        self.annuals = scenarios[scenarios.index==name].transpose().rename(columns={self.name: "target"})

        self.scalable = ["Strombedarf", "Pumpspeicher", "Laufkraft", "Windkraft", "Photovoltaik"]
        self.excel_em_prods =  {EXCEL_TO_EM_colnames[k]:k for k in self.scalable}
        self.excel_em_cons = {k.replace("production", "consumption"):v for k,v in self.excel_em_prods.items()}

        self.base_df = pd.DataFrame()
        self.base_year = None
        self.load_base(em_base)

        self.TSD = pd.DataFrame() # the current time step data of the scenario
        self.reset()

        if transformation_scenario is None:
            self.transformations = []
        else:
            self.transformations = transformation_scenario
            self.apply(self.transformations)

        self.res_column = "RES1"
        #"RES0" =  Volatile EE (laufkraft, Wind, PV) - Strombedarf
        #"RES1" =  Volatile EE (laufkraft, Wind, PV) - Strombedarf - pumpspeicher
        #"RES2" =  Volatile EE (laufkraft, Wind, PV) - Strombedarf - pumpspeicher - nicht-volatile (biomasse, )
        self.signal_column = "RES1"
        self.signal_separator = 0.5
        self.define_signal()

        self.winter = ((self.RES.index.month <= 3) | (self.RES.index.month >= 10))
        self.summer = ((self.RES.index.month <= 9) | (self.RES.index.month >= 4))

    def reset(self):
        "resets the scneario to its base scaling, resetting any transformations"

        self._scale_base_to_target()
        self._recalc()

    def _recalc(self):
        self.TSD["Volatile EE"] = self.TSD["Laufkraft"] \
                                + self.TSD["Windkraft"] \
                                + self.TSD["Photovoltaik"]
        self.TSD["Erzeugung"] = self.TSD["Pumpspeicher"] + self.TSD["Volatile EE"]
        self.TSD["RES0"] = self.TSD["Volatile EE"] - self.TSD["Strombedarf"]
        self.TSD["RES1"] = self.TSD["RES0"] + self.TSD["Pumpspeicher"]



        self.daily = self.TSD.resample("D")
        self.weekly = self.TSD.resample("W")
        self.monthly = self.TSD.resample("M")

        self.daily_mean = self.daily.mean()
        self.weekly_mean = self.weekly.mean()
        self.monthly_mean = self.monthly.mean()


    def apply(self, traffo_scenario, reset=False):
        "applies a transformation scenario to the TSD of the scenario"
        if reset:
            self.reset()
        for transformation in traffo_scenario:
            self.apply_transform(transformation)
        self._recalc()

    def apply_transform(self, transformation:traffo.Transformation):
        if type(transformation) is not traffo.Transformation:
            raise TypeError(f"Transformation type {traffo.Transformation} expected, got {type(transformation)} ")
        kind = transformation.kind
        if kind not in self.scalable:
            raise ValueError(f"type {kind} nicht skalierbar für scenario (verfügbar: {self.scalable}")

        self.TSD[kind] = transformation.apply(self.TSD[kind])


    def load_base(self, em_base):
        """
        loads an electricity map year as .em_base
        :param em_base: a year of electricity map data as dict with {year, df}
        :return:
        """
        self.base_df = em_base["df"]
        self.base_year = em_base["year"]
        self.annuals["base"] = em_base["df"][self.em_excel.keys()].rename(columns={k: v for k, v in zip(self.em_excel, self.scalable)}).sum() / 1000
        self.annuals.loc["Jahr", "base"] = self.base_year
        self._calc_scale()

    def _calc_scale(self):
        for scale in self.scalable:
            self.annuals.loc[scale,
                             "scale"] = self.annuals.loc[scale,"target"] / self.annuals.loc[scale,"base"]

    def _scale_base_to_target(self):
        for scale in self.scalable:
            f = self.annuals.loc[scale, "scale"]
            self.TSD[scale] = f * self.base_df[self.excel_em[scale]]
        self.TSD = self.TSD/1000

    @property
    def demand_supply(self):
        return self.TSD[self.scalable]

    @property
    def demand(self):
        return self.TSD["Strombedarf"]

    @property
    def supplies(self):
        return self.TSD[self.scalable].drop("Strombedarf", axis=1)

    @property
    def RES(self):
        """returns the REsidualload from Volatiles (RES0) or from all renewables (RES1) as timeseries"""
        return self.TSD[self.res_column]

    @property
    def monthly_mismatch(self):
        """Verhältnis Erzeugung (alle EE) zu Strombedarf """
        rs = self.TSD.resample("M").sum()
        return rs["Erzeugung"] / rs["Strombedarf"]

    @property
    def seasonal_mismatch(self):
        """Verhältnis Residuallast Sommer(m4-9) zu winter (m10-3)"""
        winter_mask = ((self.RES.index.month <= 3) | (self.RES.index.month >= 10))
        summer_mask = ((self.RES.index.month <= 9) | (self.RES.index.month >= 4))
        return self.RES[summer_mask].mean() / self.RES.mean()

    @property
    def signal(self):
        """Signal: 'scenario.signal_column' TSD mit scenario.signal_separator diskretisiert """
        n = traffo.normalize(pd.DataFrame(self.TSD[self.signal_column], index=self.RES.index))
        d = traffo.discretize(n, separator=self.signal_separator)
        return d[self.signal_column]

    def define_signal(self, column="RES1", separator=0.5):
        """Festlegung, welcher TSD Spaltenname
        mit welchem Separator zum Signal diskretisiert wird"""
        self.signal_column = column
        self.signal_separator = separator

    @property
    def signal_properties(self):
        """:returns df mit einer Zeile für das derzeitige Signal mit
        Anzahl und durchschnittloicer Längeder Freigabezeiten"""
        return fps.signal_properties(pd.DataFrame(self.signal, index=self.signal.index), 0.5)

    @property
    def signal_props_summerwinter(self):
        """:returns df mit einer Zeile je Sommer und Winter für das derzeitige Signal mit
        Anzahl und durchschnittloicer Längeder Freigabezeiten"""
        sig_s, sig_w = fps.signal_properties_s(pd.DataFrame(self.signal, index=self.signal.index), 0.5)
        props = sig_w.append(sig_s)
        props.index = ["Winter", "Sommer"]
        return props


    @property
    def em_excel(self):
        if self.base_year >= 2018:
            return self.excel_em_prods
        elif 2015 <= self.base_year <= 2017:
            return self.excel_em_cons

    @property
    def excel_em(self):
        return {v: k for k,v in self.em_excel.items()}

    def plot(self):
        """plots the scenario volatile RE and demand as well as the resulting residual load tsd"""
        # fig, ax = plt.subplots(2, 1, figsize=(15, 10))

        fig = plt.figure(figsize=(15,10))
        fig.suptitle(f"Scenario {self.name}")
        ax1 = fig.add_subplot(4,1,1)
        ax2 = fig.add_subplot(4,1,2, sharex=ax1)
        ax3 = fig.add_subplot(4,1,3)
        ax4 = fig.add_subplot(4,1,4, sharex=ax3)
        ax1 = self.plot_supplydemand(ax=ax1, hourly=True, daily=False, weekly=False)
        ax1.legend(["Bedarf", "Volatile EE"])
        ax2 = self.plot_supplydemand(ax=ax2, hourly=False, daily=True, weekly=True)
        ax2.legend(["Tagesmittel", "Wochenmittel"])
        ax1.set_ylim(0,max(self.TSD["Volatile EE"]))
        ax2.set_ylim(0,max(self.TSD["Volatile EE"]))
        ax3 = self.plot_heatmap(self.RES, ax=ax3, cbar=False, cmap="PiYG")
        ax4 = self.plot_heatmap(self.signal, ax=ax4, cbar=False, cmap="bone")
        ax3.set_title("Residuallast")
        ax4.set_title(">0")
        # fig.tight_layout()
        return fig, [ax1,ax2,ax3,ax4]

    def plot_energy_mix(self):
        fig, ax = plt.subplots(1,3, figsize=(15,5), sharey=True,
                               gridspec_kw={'width_ratios':[4,1,1]})

        fpp.plot_annual_w_seasonal_detail(
            df=self.supplies,
            fig=fig, ax=ax,
            legend=True,
            stacked=True,
            kind="area",
            color=config.COLORS
        )
        fpp.plot_annual_w_seasonal_detail(
            df=self.demand,
            fig=fig, ax=ax,
            legend=True,
            stacked=False,
            color=config.COLORS,
        )

        return fig, ax

    def plot_signal(self, ax=None, legend=True):
        """plots heatmap, #of signal hours and average time
        for current signal in a row"""
        if ax is None:
            fig, ax = plt.subplots(1,3, figsize=(15,5), gridspec_kw={'width_ratios':[4,1,1]})

        self.plot_heatmap(self.signal, ax=ax[0], cbar=False, cmap="bone")
        self.signal_props_summerwinter[["Zeitraum mit Signal [h]", "Nicht-Signal-Zeitraum [h]"]] \
            .plot(ax=ax[1], kind="bar", color=["Yellowgreen", "Purple"],stacked=True, legend=False) \
            .set(ylabel="Stunden")

        for p in ax[1].patches:
            ax[1].annotate("{:.0f}".format(p.get_height()),
                           (p.get_x() + p.get_width() / 2., p.get_height() + p.get_y() - 5), ha='center', va='center',
                           fontsize=17, color='black', xytext=(0, -8), textcoords='offset points')

        ax[1].yaxis.set_ticks(np.arange(0, 6000, 24*30))


        self.signal_props_summerwinter[["Durchschnittliche Dauer Signal [h]", "Durchschnittliche Dauer Nicht-Signal [h]"]] \
            .plot(ax=ax[2], kind="bar", color=["Yellowgreen", "Purple"], stacked=False, legend=False) \
            .set(ylabel="Stunden")
        for p in ax[2].patches:
            ax[2].annotate("{:.0f}".format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center',
                           va='center', fontsize=17, color='black', xytext=(0, 4), textcoords='offset points')
        ax[2].yaxis.set_ticks(np.arange(0, 169, 24))

        ax[1].get_xaxis().set_visible(False)
        ax[1].get_yaxis().set_visible(False)
        ax[2].get_xaxis().set_visible(False)
        ax[2].get_yaxis().set_visible(False)
        if legend:
            ax[1].get_xaxis().set_visible(True)
            ax[1].get_yaxis().set_visible(True)
            ax[2].get_xaxis().set_visible(True)
            ax[2].get_yaxis().set_visible(True)
            ax[1].legend(["Freigabe", "Keine"])
            ax[2].legend(["Freigabe", "Keine"])
            ax[1].set_title("Freigabezeitraum")
            ax[2].set_title("Mittlere Signallänge")


        # if cut_ylim:
        #     plt.ylim(top=cut_ylim)
        # plt.grid(axis="x")
        return ax

    def plot_heatmap(self, series, ax=None, **heatmap_args):
        """wrapper for fpp.heatmap_ax for a given series"""
        if ax is None:
            fig, ax = plt.subplots(1, 1)
        ax = fpp.heatmap_ax(series=series, ax=ax, **heatmap_args)
        return ax

    def plot_supplydemand(self, ax, hourly=False, daily=False, weekly=False, monthly=False, **kwargs):
        """generic annual supply demand plot with configurable time aggregation"""
        columns = ["Strombedarf", "Erzeugung"]

        for c in columns:
            if hourly:
                self.TSD[c].plot(ax=ax, color=config.COLORS[c], marker='.', alpha=0.2, linestyle='None', legend=False, **kwargs)
            if daily:
                self.daily_mean[c].plot(ax=ax, color=config.COLORS[c], linewidth=0.5, alpha=0.5, **kwargs)
            if weekly:
                self.weekly_mean[c].plot(ax=ax, color=config.COLORS[c], linewidth=1.5, alpha=0.8, **kwargs)
            if monthly:
                self.monthly_mean[c].plot(ax=ax, color=config.COLORS[c], linewidth=2.5, alpha=1, drawstyle="steps", **kwargs)

        # self.weekly_mean["Strombedarf"].plot(color="black", linewidth=1.5, ax=ax)
        # self.weekly_mean["Volatile EE"].plot(color="green", linewidth=1.5, ax=ax)
        # self.weekly_mean["Erzeugung"].plot(color="cyan", linewidth=1.5, ax=ax, drawstyle="steps")
        # df_monthly[["carbon_intensity_avg"]].plot(color="gray", ax=ax2)
        # ax.set_xlabel("")

        ax.set_ylabel("GW")

        ax.set_xlim(self.TSD.index[0], self.TSD.index[-1])
        return ax

    def plot_monthly_mismatch(self, ax=None, hourly=False, daily=False, weekly=True, monthly=True):
        """currently bar chart """
        #TODO generalize for different time aggregations
        if ax is None:
            fig, ax = plt.subplots(1, 1)
        if hourly:
            pass
            # self.RES.plot(ax=ax, color=config.COLORS[c], marker='.', alpha=0.2, linestyle='None', legend=False)
        if daily:
            pass
            # self.RES.resample("D")..plot(ax=ax, color=config.COLORS[c], linewidth=0.5, alpha=0.5)
        if weekly:
            pass
            # self.weekly_mean[c].plot(ax=ax, color=config.COLORS[c], linewidth=1.5, alpha=0.8)
        if monthly:
            self.monthly_mismatch.plot(ax=ax, kind="bar", linewidth=2.5, alpha=1)
        ax.set_ylim(0,2)
        return ax

    def plot_transformation_scenario(self, ax=None):
        pass

    def __repr__(self):
        repr = ""
        repr += self.name + "\n" * 2
        repr += str(self.annuals)
        return repr

    def __str__(self):
        return self.repr()

    def scaling_targets(self):
        pass

