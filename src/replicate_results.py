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
    
    cmdty_df = prep_df
    
    #Get Commodities which have more than 1 contracts against the same date
    cmdtry_cntrct_count = cmdty_df.groupby(['Commodity', 'Date'])['Contract'].nunique().reset_index(name='Distinct_Contracts')
    cmdtry_cntrct_atlst_2 = cmdtry_cntrct_count[cmdtry_cntrct_count['Distinct_Contracts'] > 1]
    
    #Get list of the commodities for the aforementioned criterion
    list_of_commodities = cmdtry_cntrct_atlst_2['Commodity'].unique()
    
    #Filter the data to only get the subset of interest
    cmdty_entire_df = cmdty_df[cmdty_df['Commodity'].isin(list_of_commodities)]
    cmdty_entire_df.reset_index(inplace = True)

    #Getting Close Prices for 1st to Expire Contract Per Commodity
    cmdty_cntrct_first_to_expire_df = cmdty_entire_df[cmdty_entire_df['Contract'] == first_to_exp_ind]
    max_date_price_first_exp = cmdty_cntrct_first_to_expire_df.groupby(['Commodity', 'YearMonth']).apply(
                                lambda x: x.loc[x['Date'].idxmax(), ['Date', 'Contract', 'ClosePrice']]).reset_index()
    max_date_price_first_exp['uid'] = max_date_price_first_exp['Commodity'] + max_date_price_first_exp['Date'].astype(str) + max_date_price_first_exp['Contract'].astype(str)
    max_date_price_first_exp.sort_values(by=['Commodity','YearMonth'], inplace =True)
    #max_date_price_first_exp.set_index('Date', inplace=True)

    #### Last to Expire ####
    #Getting Close Prices for Last to Expire Contract per Commodity
    cmdty_cntrct_last_to_expire_df = cmdty_entire_df[cmdty_entire_df['Contract'] > first_to_exp_ind]
    max_date_cntrct_last_exp_df = cmdty_cntrct_last_to_expire_df.groupby(['Commodity', 'YearMonth']).agg(Max_Date=('Date', 'max'),
                                                                                         Max_Contract_Number=('Contract', 'max')).reset_index()
    
    cmdty_entire_df_temp = cmdty_entire_df
    cmdty_entire_df_temp['uid'] = cmdty_entire_df_temp['Commodity'] + cmdty_entire_df_temp['Date'].astype(str) + cmdty_entire_df_temp['Contract'].astype(str)
    max_date_cntrct_last_exp_df['uid'] = max_date_cntrct_last_exp_df['Commodity'] + max_date_cntrct_last_exp_df['Max_Date'].astype(str) + max_date_cntrct_last_exp_df['Max_Contract_Number'].astype(str)
    max_date_cntrct_last_exp_price_df = pd.merge(max_date_cntrct_last_exp_df, cmdty_entire_df_temp[['uid','ClosePrice']], how = 'left', left_on = 'uid', right_on='uid')

    max_date_price_first_exp.drop(columns = ['uid'],inplace = True)
    max_date_price_first_exp.reset_index()
    
    max_date_cntrct_last_exp_price_df.drop(columns = ['uid'], inplace=True)
    max_date_cntrct_last_exp_price_df.reset_index()

    if last_to_expire == False:
        return max_date_price_first_exp
    else:
        return max_date_cntrct_last_exp_price_df

def compute_basis_timeseries(prep_df):
    first_to_expire = get_first_last_to_expire_contract(prep_df, 1, False)
    first_to_expire['uid'] = first_to_expire['Commodity'] + first_to_expire['Date'].astype(str)

    last_to_expire = get_first_last_to_expire_contract(prep_df, 1, True)
    last_to_expire['uid'] = last_to_expire['Commodity'] + last_to_expire['Max_Date'].astype(str)

    basis_df_base = pd.merge(first_to_expire, last_to_expire[['uid','Max_Contract_Number','ClosePrice']], how='left', left_on = 'uid', right_on = 'uid')
    basis_df_base.rename(columns={'ClosePrice_x':'ClosePriceFstExp',
                                  'ClosePrice_y':'ClosePriceLstExp'}, inplace = True)
    basis_df_base['LogClosePriceFstExp'] = np.log(basis_df_base['ClosePriceFstExp'])
    basis_df_base['LogClosePriceLstExp'] = np.log(basis_df_base['ClosePriceLstExp'])
    basis_df_base['LogPriceDiff'] = basis_df_base['LogClosePriceFstExp'] - basis_df_base['LogClosePriceLstExp']
    basis_df_base['ExpDiff'] = basis_df_base['Max_Contract_Number'] - basis_df_base['Contract']
    basis_df_base['Basis'] = basis_df_base['LogPriceDiff'] / basis_df_base['ExpDiff']
    basis_df_base.set_index('Date', inplace = True)

    return basis_df_base

def compute_basis_mean(timeseries_basis):
    mean_basis = timeseries_basis.groupby(['Commodity'])['Basis'].mean()
    return mean_basis

def compute_freq_backwardation(timeseries_basis):
    #timeseries_basis
    pass

# if __name__ == '_main_':
DATA_DIR = Path(config.DATA_DIR)
df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv")
pre_processed_df = data_preprocessing.preprocess_data(df)
returns_df = compute_commodity_excess_returns(pre_processed_df)
perf_metrics = compute_performance_metrics(returns_df)
#basis = compute_basis(pre_processed_df)
ts = get_first_last_to_expire_contract(pre_processed_df, 1, last_to_expire = True)
bob = compute_basis_timeseries(pre_processed_df)
basis = compute_basis_mean(bob)
print(basis)
