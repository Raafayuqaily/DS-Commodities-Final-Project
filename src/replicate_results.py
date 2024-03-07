# This python file is designed to compute the required metrics
# and poppulate and return a dataframe that replicates Table 1 from the study

import warnings
warnings.filterwarnings("ignore")

import load_commodities_data
import data_preprocessing
import config
from pathlib import Path
import pandas as pd
import numpy as np


DATA_DIR = Path(config.DATA_DIR)
df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv")
pre_processed_df = data_preprocessing.preprocess_data(df)

def compute_num_observations(prep_df):
    """
    Computing average monthly observations
    """
    df = prep_df
    df.reset_index(inplace=True)
    total_cmdty_obs = df.groupby(['Commodity'])['Date'].count()
    total_cmdty_mths = df.groupby(['Commodity'])['YearMonth'].nunique()
    obs_df = pd.merge(total_cmdty_obs, total_cmdty_mths, how='left', left_on='Commodity', right_on='Commodity')
    obs_df.rename(columns={'Date':'Total_Observations', 'YearMonth':'NumMths'}, inplace=True)
    obs_df['N'] = obs_df['Total_Observations'] / obs_df['NumMths']
    return obs_df['N']

def compute_commodity_excess_returns(prep_df):
    """
    Computing Historical Excess Returns for Futures
    """
    cmdty_cntrct_2_df = prep_df[prep_df['Contract']==2]
    cmdty_cntrct_2_df.reset_index(inplace = True)
    max_date_px_last_cntrct_2 = cmdty_cntrct_2_df.groupby(['Commodity', 'YearMonth']).apply(
                                lambda x: x.loc[x['Date'].idxmax(), ['Date', 'Close_Price']]).reset_index()
    max_date_px_last_cntrct_2.sort_values(by=['Commodity','YearMonth'], inplace =True)
    max_date_px_last_cntrct_2.set_index('Date', inplace=True)
    max_date_px_last_cntrct_2_pivot = max_date_px_last_cntrct_2.pivot_table(index = 'Date', columns = 'Commodity', values = 'Close_Price')
    cmdty_cntrct_2_rets_df = max_date_px_last_cntrct_2_pivot.pct_change()
    return cmdty_cntrct_2_rets_df

def compute_performance_metrics(excess_returns_df, annualizing_period = 12):
    """
    Input:
        1. DataFrame of Historical Excess Returns
        2. Annualizing Period, default value set to 12 (Convert Monthly to Yearly)
    
    Output:DataFrame for Performance Metrics: 
                    1. Annualized Mean, 
                    2. Annualized Vol, 
                    3. Annualized Sharpe Ratio
    """
    avg_hist_excess_returns = excess_returns_df.mean() * annualizing_period * 100
    std_hist_excess_returns = excess_returns_df.std() * np.sqrt(annualizing_period) * 100
    sharpe_ratio = avg_hist_excess_returns/std_hist_excess_returns
    performance_metrics = pd.DataFrame({"Annualized Hist Avg Excess Returns": avg_hist_excess_returns, 
                                        "Annualized Hist Avg Volatility": std_hist_excess_returns, 
                                        "Annualized Sharpe Ratio": sharpe_ratio})
    return performance_metrics

def compute_basis(prep_df):

    cmdty_entire_df = prep_df.reset_index()

    #Computing Returns for 1st to Expire Contract Per Commodity
    cmdty_cntrct_1_df = cmdty_entire_df[cmdty_entire_df['Contract']==1]
    #cmdty_cntrct_1_df.reset_index(inplace = True)
    max_date_px_last_cntrct_1 = cmdty_cntrct_1_df.groupby(['Commodity', 'YearMonth']).apply(
                                lambda x: x.loc[x['Date'].idxmax(), ['Date', 'Close_Price']]).reset_index()
    max_date_px_last_cntrct_1.sort_values(by=['Commodity','YearMonth'], inplace =True)
    max_date_px_last_cntrct_1.set_index('Date', inplace=True)

    #Computing Returns for Last to Expire Contract per Commodity
    #cmdty_entire_df_last_exp = cmdty_entire_df.reset_index()
    max_contract_px_last = cmdty_entire_df.groupby(['Commodity','YearMonth']).apply(
                        lambda x: x.loc[x['Contract'].idxmax()]).reset_index(drop=True)
    max_contract_px_last = max_contract_px_last[max_contract_px_last['Contract'] > 1]
    max_contract_px_last.sort_values(by=['Commodity', 'YearMonth'], inplace=True)
    max_contract_px_last.set_index('Date', inplace=True)

    max_date_px_last_cntrct_1.reset_index(inplace=True)
    max_contract_px_last.reset_index(inplace=True)

    cmdty_cntrct_1_and_latest_df = pd.merge(max_date_px_last_cntrct_1, max_contract_px_last, how='left', left_on=['Commodity', 'YearMonth'], right_on=['Commodity', 'YearMonth'])
    return cmdty_cntrct_1_and_latest_df

def compute_freq_backwardation(computed_basis):
    pass

# if __name__ == '_main_':
DATA_DIR = Path(config.DATA_DIR)
df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv")
pre_processed_df = data_preprocessing.preprocess_data(df)
returns_df = compute_commodity_excess_returns(pre_processed_df)
perf_metrics = compute_performance_metrics(returns_df)
basis = compute_basis(pre_processed_df)
print(basis)