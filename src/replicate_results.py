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
                                lambda x: x.loc[x['Date'].idxmax(), ['Date', 'ClosePrice']]).reset_index()
    max_date_px_last_cntrct_2.sort_values(by=['Commodity','YearMonth'], inplace =True)
    max_date_px_last_cntrct_2.set_index('Date', inplace=True)
    max_date_px_last_cntrct_2_pivot = max_date_px_last_cntrct_2.pivot_table(index = 'Date', columns = 'Commodity', values = 'ClosePrice')
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

def get_first_last_to_expire_contract(prep_df, first_to_exp_ind = 1, last_to_expire = False):

    cmdty_entire_df = prep_df.reset_index()
    
    #Getting Close Prices for 1st to Expire Contract Per Commodity
    cmdty_cntrct_first_to_expire_df = cmdty_entire_df[cmdty_entire_df['Contract'] == first_to_exp_ind]
    max_date_price_first_exp = cmdty_cntrct_first_to_expire_df.groupby(['Commodity', 'YearMonth']).apply(
                                lambda x: x.loc[x['Date'].idxmax(), ['Date', 'ClosePrice']]).reset_index()
    max_date_price_first_exp['Contract'] = first_to_exp_ind
    max_date_price_first_exp.sort_values(by=['Commodity','YearMonth'], inplace =True)
    max_date_price_first_exp.set_index('Date', inplace=True)

    #Getting Close Prices for Last to Expire Contract per Commodity
    cmdty_cntrct_last_to_expire_df = cmdty_entire_df[cmdty_entire_df['Contract'] > first_to_exp_ind]
    max_price_last_exp = cmdty_cntrct_last_to_expire_df.groupby(['Commodity', 'YearMonth']).apply(
                    lambda x: x.loc[x['Date'].idxmax()]).reset_index(drop=True)
    max_price_last_exp.sort_values(by=['Commodity', 'YearMonth'], inplace=True)
    print(max_price_last_exp)
    #max_price_last_exp.set_index('Date', inplace=True)

    if last_to_expire == False:
        return max_date_price_first_exp
    else:
        return max_price_last_exp

def compute_basis(prep_df, first_to_exp_ind = 1, last_to_expire = False):

    first_to_expire_df = get_first_last_to_expire_contract(prep_df, first_to_exp_ind, last_to_expire = last_to_expire)
    last_to_expire_df = get_first_last_to_expire_contract(prep_df, first_to_exp_ind, last_to_expire = True)

    first_to_expire_df.reset_index(inplace = True)
    last_to_expire_df.reset_index(inplace = True)

    cmdty_exp_df = pd.merge(first_to_expire_df, last_to_expire_df, how='left', left_on=['Commodity', 'YearMonth'], right_on=['Commodity', 'YearMonth'])
    cmdty_exp_df = cmdty_exp_df.rename(columns={'Date_x':'Date',
                                                'ClosePrice_x':'ClosePriceFrstExp',
                                                'ClosePrice_y':'ClosePriceLastExp',
                                                'Contract_x':'FirstToExp',
                                                'Contract_y':'LastToExp'})
    cmdty_exp_df.drop(columns=['Date_y'], inplace = True)
    cmdty_exp_df['LogFrstToExp'] = np.log(cmdty_exp_df['ClosePriceFrstExp'])
    cmdty_exp_df['LogLastToExp'] = np.log(cmdty_exp_df['ClosePriceLastExp'])
    

    return cmdty_exp_df

def compute_freq_backwardation(computed_basis):
    pass

# if __name__ == '_main_':
DATA_DIR = Path(config.DATA_DIR)
df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv")
pre_processed_df = data_preprocessing.preprocess_data(df)
returns_df = compute_commodity_excess_returns(pre_processed_df)
perf_metrics = compute_performance_metrics(returns_df)
#basis = compute_basis(pre_processed_df)
ts = get_first_last_to_expire_contract(pre_processed_df, 1, last_to_expire = True)
print((ts.loc[ts['Commodity'] == 'Aluminium', 'Contract']))
