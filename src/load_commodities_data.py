"""
This module is designed for loading and initial processing of commodity data stored in a local directory. 
It includes functionality to load data from a specified CSV file and logs the status of data loading.
"""

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
    Load commodity data from a specified file within a specified directory.
    
    Parameters:
        data_dir (str): Directory where the data file is stored.
        input_file (str): Name of the file to load.
        
    Returns:
        pandas.DataFrame: Data frame containing the loaded commodity data.
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