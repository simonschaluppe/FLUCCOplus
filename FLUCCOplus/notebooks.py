from FLUCCOplus.utils import *
from FLUCCOplus.config import *
import os
# plt.style.use('fivethirtyeight')

import seaborn as sns
sns.set_style("whitegrid")

sns.set_context("paper",
                font_scale=1.,
                rc={"lines.linewidth": 0.7})

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

if not os.path.exists("..\data\Plots"):
        os.makedirs("..\data\Plots")

if VERBOSE:
    print(__name__, "loaded!")