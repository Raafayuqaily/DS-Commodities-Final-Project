"""
This module is designed to test the data preprocessing functionalities provided by the 
data_preprocessing module. It checks if the data types, sorting, and column names of 
the processed data match expected outcomes.
"""

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
    """
    Tests the types of the columns in the processed data to ensure they match expected types.
    Specifically, it checks that the 'ClosePrice' column is of type float, the 'Contract' column 
    is of type int, and the DataFrame index is of datetime type.
    """

    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that data types are as expected after preprocessing
    assert processed_data['ClosePrice'].dtype == float
    assert processed_data['Contract'].dtype == int
    assert processed_data.index.dtype == '<M8[ns]'

def test_preprocess_data_sorting():
    """
    Tests that the processed data is sorted correctly.
    It verifies that the DataFrame index (which should be dates) is sorted in ascending order.
    """

    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that the data is sorted correctly after preprocessing
    assert (processed_data.index == processed_data.index.sort_values()).all()

def test_preprocess_data_column_names():
    """
    Tests that the processed data contains all expected columns after preprocessing.
    It checks for the presence of 'Commodity', 'Contract', 'ClosePrice', and 'YearMonth' columns.
    """
    processed_data = data_preprocessing.clean_process_data(start_date = STARTDATE, end_date = ENDDATE, data_dir = DATA_DIR, input_file = INPUTFILE)

    # Test that column names are as expected after preprocessing
    expected_columns = ['Commodity', 'Contract', 'ClosePrice', 'YearMonth']
    assert all(col in processed_data.columns for col in expected_columns)

if __name__ == "__main__":
    pytest.main()
