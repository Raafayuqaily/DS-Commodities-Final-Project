#This Python file loads the data from the drive
#Cleans and Processes the data as per the requirement

import pandas as pd
import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
file_ = config.FILENAME
STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD

def load_data(data_dir = DATA_DIR, file_name = file_):
    """
    Input:
        1. Data Directory, where the data is stored
        2. file_name = file that the user wants to load (Commodities in our case)
    
    Output:
        DataFrame created by reading the csv
    """
    file_path = Path(data_dir) / "manual" / file_name
    df = pd.read_csv(file_path)
    return df

def clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, file_name = file_):
    """
    Inputs:
        1. start_date, format: 'YYYY-MM-DD', default: config.py->STARTDATE_OLD
        2. end_date, format: 'YYYY-MM-DD', default: config.py->ENDDATE_OLD
        3. data_dir, format: str, default: config.py->DATADIR
        4. file_name, format: str, default: config.py->FILENAME
    Output:
        Clean DataFrame for Close Prices
    """
    
    #loading base data
    base_data_df = load_data(DATA_DIR, file_)

    #Changing Column name from PX_LAST to ClosePrice
    base_data_df.rename(columns = {'PX_LAST':'ClosePrice'}, inplace = True)
    
    #Ensuring Variable Types are as required for analysis
    base_data_df['Date'] = pd.to_datetime(base_data_df['Date'])
    base_data_df['Contract'] = base_data_df['Contract'].astype(int)
    base_data_df['ClosePrice'] = base_data_df['ClosePrice'].astype(float)

    #Creating a column for YearMonth, which makes analysis easier
    base_data_df['YearMonth'] = base_data_df['Date'].dt.to_period('M')
    
    #Filtering out Commodities with data inconsistencies on Bloomberg
    commodities_to_drop = ['Barley', 'Coal', 'Propane', 'Broilers', 'Butter']
    base_data_df = base_data_df[~base_data_df['Commodity'].isin(commodities_to_drop)]
    
    #Sorting the dataframe and setting Date as index
    base_data_df.sort_values(by=['Date','Commodity'], inplace = True)
    base_data_df.set_index('Date', inplace = True)

    #Filtering Data for Start and End Date (User Defined, otherwise default)
    final_df = base_data_df[start_date:end_date]

    return final_df
