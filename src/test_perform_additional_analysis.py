import os
import pytest
import pandas as pd
import config
from pathlib import Path

import perform_additional_analysis as paa
import load_commodities_data as lcd
import data_preprocessing as dp

DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)


def test_plot_commodities_by_sector():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_commodities_by_sector(df, output_dir)
    assert os.path.exists(output_dir.join("commodities_by_sector.png"))


def test_plot_data_availability():
    
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_data_availability(df, output_dir)
    assert os.path.exists(output_dir.join("data_availability_heatmap.png"))


def test_plot_max_contract_number():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_max_contract_number(df, output_dir)
    assert os.path.exists(output_dir.join("maximum_contract_number.png"))


def test_plot_max_contract_availability():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_max_contract_availability(df, output_dir)
    assert os.path.exists(output_dir.join("max_contract_availability.png"))


def test_plot_commodity_time_series(df):

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_commodity_time_series(df, output_dir, commodity='A')
    assert os.path.exists(output_dir.join("A_futures_contracts_time_series.png"))


def test_plot_return_distribution_and_save_formatted_stats():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_return_distribution_and_save_formatted_stats(df, output_dir, contract_num=1)
    assert os.path.exists(output_dir.join("monthly_returns_distribution_contract_1.png"))
    assert os.path.exists(output_dir.join("monthly_returns_stats_contract_1.tex"))


def test_plot_rolling_volatility():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_rolling_volatility(df, output_dir, rolling_window=60, contract_num=1)
    assert os.path.exists(output_dir.join("60_months_rolling_volatility.png"))


def test_plot_rolling_sharpe_ratio():

    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_rolling_sharpe_ratio(df, output_dir, rolling_window=60, contract_num=1)
    assert os.path.exists(output_dir.join("60_months_rolling_sharpe_ratio.png"))

if __name__ == '__main__':
    pytest.main()
