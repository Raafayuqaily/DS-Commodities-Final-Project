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
    assert (output_dir / "commodities_by_sector.png").is_file()


def test_plot_data_availability():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_data_availability(df, output_dir)
    assert (output_dir / "data_availability_heatmap.png").is_file()


def test_plot_max_contract_number():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_max_contract_number(df, output_dir)
    assert (output_dir / "maximum_contract_number.png").is_file()


def test_plot_max_contract_availability():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    paa.plot_max_contract_availability(df, output_dir)
    assert (output_dir / "max_contract_availability.png").is_file()


def test_plot_commodity_time_series():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    commodity = 'A'  # You need to specify the commodity for this test
    paa.plot_commodity_time_series(df, output_dir, commodity=commodity)
    assert (output_dir / f"{commodity}_futures_contracts_time_series.png").is_file()


def test_plot_return_distribution_and_save_formatted_stats():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    contract_num = 1  # You need to specify the contract number for this test
    paa.plot_return_distribution_and_save_formatted_stats(df, output_dir, contract_num=contract_num)
    assert (output_dir / f"monthly_returns_distribution_contract_{contract_num}.png").is_file()
    assert (output_dir / f"monthly_returns_stats_contract_{contract_num}.tex").is_file()


def test_plot_rolling_volatility():
    df = lcd.load_data(data_dir=DATA_DIR, file_name="commodities_data_2024.csv")
    df = dp.preprocess_data(df)
    output_dir = Path(config.OUTPUT_DIR)

    rolling_window = 60  # You need to specify the rolling window for this test
    contract_num = 1  # You need to specify the contract number for this test
    paa.plot_rolling_volatility(df, output_dir, rolling_window=rolling_window, contract_num=contract_num)
    assert (output_dir / f"{rolling_window}_months_rolling_volatility.png").is_file()


if __name__ == '__main__':
    pytest.main()

