# This Python file is designed to load data from the local drive

#This Python file loads the data from the drive
#Cleans and Processes the data as per the requirement
import warnings
import logging
warnings.filterwarnings("ignore")

import pandas as pd
import config
from pathlib import Path

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE

def load_data(data_dir = DATA_DIR, input_file = INPUTFILE):
    """
    Input:
        1. Data Directory, where the data is stored
        2. file_name = file that the user wants to load (Commodities in our case)
    
    Output:
        DataFrame created by reading the csv
    """
    file_path = Path(data_dir) / "manual" / input_file
    try:
        df = pd.read_csv(file_path)
        logging.info("Commodities Data loaded successfully!")
        return df
    except Exception as e:
        logging.error(f"An error occurred while loading the data: {e}")
        raise e

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        df = load_data(DATA_DIR, INPUTFILE)
    except Exception as e:
        logging.error(f"Failed to load data: {e}")