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

INPUTFILE = config.INPUTFILE
STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD


def test_plot_commodities_by_sector():
    df = lcd.load_data(DATA_DIR)  # Make sure this returns the expected DataFrame
    # Now using clean_process_data
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR, input_file=INPUTFILE)
    output_dir = Path(config.OUTPUT_DIR)
    
    paa.plot_commodities_by_sector(df, output_dir)
    assert (output_dir / "commodities_by_sector.png").is_file()


def test_plot_data_availability():
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_data_availability(df, output_dir)
    assert (output_dir / "data_availability_heatmap.png").is_file()

def test_plot_max_contract_number():
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_max_contract_number(df, output_dir)
    assert (output_dir / "maximum_contract_number.png").is_file()

def test_plot_max_contract_availability():
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_max_contract_availability(df, output_dir)
    assert (output_dir / "max_contract_availability.png").is_file()

def test_plot_commodity_time_series():
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    commodity = 'Aluminium'  # Example, change as needed
    paa.plot_commodity_time_series(df, output_dir, commodity=commodity)
    assert (output_dir / f"{commodity}_futures_contracts_time_series.png").is_file()

def test_plot_rolling_volatility():
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    rolling_window = 60  # Specify the rolling window for this test
    contract_num = 1  # Specify the contract number for this test
    paa.plot_rolling_volatility(df, output_dir, rolling_window=rolling_window, contract_num=contract_num)
    assert (output_dir / f"{rolling_window}_months_rolling_volatility.png").is_file()

if __name__ == '__main__':
    pytest.main()

