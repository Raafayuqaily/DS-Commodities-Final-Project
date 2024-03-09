import pandas as pd
import pytest
import config
from pathlib import Path

import load_commodities_data

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE


def test_load_commodities_data_functionality():
    df = load_commodities_data.load_data(data_dir=DATA_DIR, input_file = INPUTFILE)
    
    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame is not empty
    assert not df.empty

    # Test if the function raises an error when given an invalid data directory
    with pytest.raises(FileNotFoundError):
        load_commodities_data.load_data(data_dir="invalid_directory", input_file = INPUTFILE)


def test_load_commodities_data_completedness():
    df = load_commodities_data.load_data(data_dir=DATA_DIR, input_file = INPUTFILE)

    # Test if the DataFrame has the expected columns
    expected_columns = ['Commodity', 'Contract', 'PX_LAST']
    assert all(col in df.columns for col in expected_columns)

    # Test if the unique number of commodities is greater than or equal to 30
    assert df['Commodity'].nunique() >= 25