import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from statsmodels.tsa.stattools import adfuller

def process_trading_data(data):
    """
    Processes the trading data DataFrame by renaming cumulative P&L columns and calculating daily P&L.

    Parameters:
        data (DataFrame): The trading data with columns for cumulative and daily P&L.
    """
    if 'option_PL' not in data.columns or 'stock_PL' not in data.columns or 'net_PL' not in data.columns:
        raise ValueError("DataFrame must contain 'option_PL', 'stock_PL', and 'net_PL' columns")

    data.rename(columns={'option_PL': 'cum_option_PL',
                         'stock_PL': 'cum_stock_PL',
                         'net_PL': 'cum_net_PL'}, inplace=True)

    data['option_PL'] = data['cum_option_PL'].diff()
    data['stock_PL'] = data['cum_stock_PL'].diff()
    data['net_PL'] = data['cum_net_PL'].diff()

    return data