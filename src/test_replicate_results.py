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
    clean_data_file_path = Path(DATA_DIR) / "manual"/f"clean_{start_}_{end_}_{INPUTFILE}"
    clean_data_df = pd.read_csv(clean_data_file_path)

    # Test if the function computes performance metrics with numerical values
    excess_returns_df = replicate_results.compute_commodity_excess_returns(clean_data_df)
    performance_metrics = replicate_results.compute_performance_metrics(excess_returns_df)
    assert performance_metrics.dtypes.apply(pd.api.types.is_numeric_dtype).all()


def test_compute_freq_backwardation():
    clean_data_file_path = Path(DATA_DIR) / "manual"/f"clean_{start_}_{end_}_{INPUTFILE}"
    clean_data_df = pd.read_csv(clean_data_file_path)

    # Test if the function computes frequency of backwardation with positive numerical values
    freq_backwardation = replicate_results.compute_freq_backwardation(clean_data_df)
    assert (freq_backwardation['Freq. of Backwardation'] > 0).all()

if __name__ == '__main__':
    pytest.main()
