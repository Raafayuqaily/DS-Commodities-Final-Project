"""
This module tests the performance metrics and backwardation frequency computation 
from the replicate_results module. It verifies that the returned values are numeric 
and that the backwardation frequency is non-negative.
"""

import pandas as pd
import pytest
import config
from pathlib import Path

import replicate_results

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE

start_ = config.STARTDATE_OLD[:4]
end_ = config.ENDDATE_OLD[:4]


def test_compute_performance_metrics():
    """
    Tests the computation of performance metrics for commodities.
    Ensures that all performance metrics computed are of numerical data types.
    """

    clean_data_file_path = Path(DATA_DIR) / "manual"/f"clean_{start_}_{end_}_{INPUTFILE}"
    clean_data_df = pd.read_csv(clean_data_file_path)

    # Test if the function computes performance metrics with numerical values
    excess_returns_df = replicate_results.compute_commodity_excess_returns(clean_data_df)
    performance_metrics = replicate_results.compute_performance_metrics(excess_returns_df)
    assert performance_metrics.dtypes.apply(pd.api.types.is_numeric_dtype).all()


def test_compute_freq_backwardation():
    """
    Tests the computation of frequency of backwardation for commodities.
    Ensures that the computed frequency of backwardation is non-negative.
    """

    clean_data_file_path = Path(DATA_DIR) / "manual"/f"clean_{start_}_{end_}_{INPUTFILE}"
    clean_data_df = pd.read_csv(clean_data_file_path)

    # Test if the function computes frequency of backwardation with positive numerical values
    freq_backwardation = replicate_results.compute_freq_backwardation(clean_data_df)
    assert (freq_backwardation['Freq. of Backwardation'] >= 0).all()

def test_sharpe_ratio_range():
    """
    Tests if the computed Sharpe Ratios are within the expected range between -100 and +100.
    This is to ensure that the Sharpe Ratio values are within a reasonable range and correctly computed.
    """

    clean_data_file_path = Path(DATA_DIR) / f"manual/clean_{start_}_{end_}_{INPUTFILE}"
    clean_data_df = pd.read_csv(clean_data_file_path)

    # Compute excess returns for the clean data
    excess_returns_df = replicate_results.compute_commodity_excess_returns(clean_data_df)

    # Compute performance metrics which include the Sharpe Ratio
    performance_metrics = replicate_results.compute_performance_metrics(excess_returns_df)

    # Assert that all Sharpe Ratio values are between -100 and +100
    assert all(-100 <= value <= 100 for value in performance_metrics['Ann. Sharpe Ratio']), "Sharpe Ratio values are out of the expected range (-100 to +100)."

if __name__ == '__main__':
    pytest.main()
