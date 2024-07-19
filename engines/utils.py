import os
import sys

sys.path.append(os.getcwd())

def rationalStrat(limit, r_shift=0, l_shift=0, risk=0, bluff=False, iniLimitMultiplier=None):
    from strategies.Strategy import Strategy

    strat = Strategy()
    strat.eval = True
    strat.r_shift = r_shift
    strat.l_shift = l_shift
    strat.risk = risk
    strat.limit = limit

    if iniLimitMultiplier:
        strat.iniLimit = True
        strat.iniLimitMultiplier = iniLimitMultiplier

    return strat