import pandas as pd
import pytest
import config
from pathlib import Path

import load_commodities_data
import data_preprocessing
import replicate_results

DATA_DIR = Path(config.DATA_DIR)

def test_compute_num_observations():

    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    prep_df = data_preprocessing.preprocess_data(df)

    # Test if the function computes the number of observations correctly
    # obs_df = replicate_results.compute_num_observations(prep_df)
    # Test if the function returns a pandas DataFrame
    # assert isinstance(obs_df, pd.DataFrame)

    # Test if the DataFrame is not empty
    # assert not obs_df.empty

    # Test if the function computes the number of observations correctly
    obs_series = replicate_results.compute_num_observations(prep_df)['N']  # Assuming 'N' is the column containing the number of observations
    # Test if the result is a pandas Series
    assert isinstance(obs_series, pd.Series)

    # Test if the Series is not empty
    assert not obs_series.empty


def test_compute_performance_metrics():

    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    prep_df = data_preprocessing.preprocess_data(df)

    # Test if the function computes performance metrics with numerical values
    excess_returns_df = replicate_results.compute_commodity_excess_returns(prep_df)
    performance_metrics = replicate_results.compute_performance_metrics(excess_returns_df)
    assert performance_metrics.dtypes.apply(pd.api.types.is_numeric_dtype).all()

def test_compute_basis_mean():

    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    prep_df = data_preprocessing.preprocess_data(df)

    # Test if the function computes basis mean with numerical values
    # basis_mean = replicate_results.compute_basis_mean(prep_df)
    # Test if the function returns a pandas DataFrame
    # assert isinstance(basis_mean, pd.DataFrame)

    # Test if the DataFrame is not empty
    # assert not basis_mean.empty

    # Test if the function computes basis mean with numerical values
    basis_mean_series = replicate_results.compute_basis_mean(prep_df)['Basis']  # Assuming 'Basis' is the column containing the basis mean
    # Test if the result is a pandas Series
    assert isinstance(basis_mean_series, pd.Series)

    # Test if the Series is not empty
    assert not basis_mean_series.empty


def test_compute_freq_backwardation():

    df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    prep_df = data_preprocessing.preprocess_data(df)

    # Test if the function computes frequency of backwardation with positive numerical values
    freq_backwardation = replicate_results.compute_freq_backwardation(prep_df)
    assert (freq_backwardation['FreqBackwardation'] > 0).all()

if __name__ == '__main__':
    pytest.main()
