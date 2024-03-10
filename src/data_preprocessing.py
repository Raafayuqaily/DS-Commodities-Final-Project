# This python file is designed to Preprocess the loaded data
# Preprocessing includes checking variable data types and sorting the data

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import config
from pathlib import Path
import load_commodities_data
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE
STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD


def clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE):
    """
    Inputs:
        1. start_date, format: 'YYYY-MM-DD', default: config.py -> STARTDATE_OLD
        2. end_date, format: 'YYYY-MM-DD', default: config.py -> ENDDATE_OLD
        3. data_dir, format: str, default: config.py -> DATADIR
        4. input_file, format: str, default: config.py -> FILENAME
    Output:
        Clean DataFrame for Close Prices
    """
    try:
        #loading base data
        base_data_df = load_commodities_data.load_data(data_dir, input_file)
    
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
    
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

    #returning the final dataframe for further analysis
    return final_df

if __name__ == '__main__':
    start_dates = [config.STARTDATE_OLD, config.STARTDATE_NEW]
    end_dates = [config.ENDDATE_OLD, config.ENDDATE_NEW]
    
    for start_, end_ in zip(start_dates, end_dates):
        logging.info(f"\nFor Time Period, {start_} to {end_}:")
        clean_df = clean_process_data(start_, end_, DATA_DIR, INPUTFILE)
        file_path = Path(DATA_DIR) / "manual" / f"clean_{start_[:4]}_{end_[:4]}_{INPUTFILE}"
        try:
            clean_df.to_csv(file_path)
            logging.info(f"clean_{start_[:4]}_{end_[:4]}_{INPUTFILE} Stored Successfully!")
        except Exception as e:
            logging.error(f"An error occurred while Storing the clean_{start_[:4]}_{end_[:4]}_{INPUTFILE}: {e}") 

