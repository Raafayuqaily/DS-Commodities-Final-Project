import pandas as pd
import pytest
import config
from pathlib import Path

import data_preprocessing

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE
STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD

def test_preprocess_data_types():
    
    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that data types are as expected after preprocessing
    assert processed_data['ClosePrice'].dtype == float
    assert processed_data['Contract'].dtype == int
    assert processed_data.index.dtype == '<M8[ns]'

def test_preprocess_data_sorting():
    
    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that the data is sorted correctly after preprocessing
    assert (processed_data.index == processed_data.index.sort_values()).all()

def test_preprocess_data_column_names():
    
    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that column names are as expected after preprocessing
    expected_columns = ['Commodity', 'Contract', 'ClosePrice', 'YearMonth']
    assert all(col in processed_data.columns for col in expected_columns)

if __name__ == "__main__":
    pytest.main()
