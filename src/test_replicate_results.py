import pandas as pd
import pytest
import config
from pathlib import Path

import load_commodities_data
import data_preprocessing
import replicate_results

DATA_DIR = Path(config.DATA_DIR)

def test_preprocess_data_types():
    
    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    processed_data = data_preprocessing.preprocess_data(df)

    # Test that data types are as expected after preprocessing
    assert processed_data['ClosePrice'].dtype == float
    assert processed_data['Contract'].dtype == int
    assert processed_data.index.dtype == '<M8[ns]'

def test_preprocess_data_sorting():
    
    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    processed_data = data_preprocessing.preprocess_data(df)

    # Test that the data is sorted correctly after preprocessing
    assert (processed_data.index == processed_data.index.sort_values()).all()

def test_preprocess_data_column_names():
    
    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    processed_data = data_preprocessing.preprocess_data(df)

    # Test that column names are as expected after preprocessing
    expected_columns = ['Commodity', 'Contract', 'ClosePrice', 'YearMonth']
    assert all(col in processed_data.columns for col in expected_columns)

if __name__ == "__main__":
    pytest.main()
