"""
This module is designed for testing the functionality and data completeness of the `load_data` function 
from the `load_commodities_data` module. It includes tests to ensure that data is correctly loaded into 
a pandas DataFrame and that the resulting DataFrame meets expected properties such as containing the 
correct columns and a sufficient variety of commodity data.
"""

import pandas as pd
import pytest
import config
from pathlib import Path

import load_commodities_data

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE
BASE_DIR = Path(__file__).resolve().parent.parent

def test_load_commodities_data_functionality():
    """
    Tests the basic functionality of the `load_data` function from the `load_commodities_data` module.

    This function checks:
    - If the returned object is a pandas DataFrame.
    - If the returned DataFrame is not empty.
    - If a FileNotFoundError is raised when an invalid directory is provided.
    """

    df = load_commodities_data.load_data(data_dir=DATA_DIR, input_file = INPUTFILE)
    
    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame is not empty
    assert not df.empty

    # Test if the function raises an error when given an invalid data directory
    with pytest.raises(FileNotFoundError):
        load_commodities_data.load_data(data_dir="invalid_directory", input_file = INPUTFILE)


def test_load_commodities_data_completedness():
    """
    Tests the data completeness for the DataFrame returned by the `load_data` function 
    from the `load_commodities_data` module.

    This function checks:
    - If the DataFrame contains specific expected columns.
    - If the DataFrame contains a sufficient variety of commodities (at least 25 unique).
    """

    df = load_commodities_data.load_data(data_dir=DATA_DIR, input_file = INPUTFILE)

    # Test if the DataFrame has the expected columns
    expected_columns = ['Commodity', 'Contract', 'PX_LAST']
    assert all(col in df.columns for col in expected_columns)

    # Test if the unique number of commodities is greater than or equal to 30
    assert df['Commodity'].nunique() >= 25

if __name__ == "__main__":
    pytest.main()
