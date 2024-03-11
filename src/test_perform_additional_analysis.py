"""
This module is designed to perform unit tests on functions within the perform_additional_analysis module.
Each function is tested to ensure that it properly generates and saves the expected plots based on the commodity data provided.
"""

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
    """
    Tests the plot_commodities_by_sector function to ensure it creates and saves the plot successfully.
    """

    df = lcd.load_data(DATA_DIR)  # Make sure this returns the expected DataFrame
    # Now using clean_process_data
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR, input_file=INPUTFILE)
    output_dir = Path(config.OUTPUT_DIR)
    
    paa.plot_commodities_by_sector(df, output_dir)
    assert (output_dir / f"commodities_by_sector_{STARTDATE}.png").is_file()


def test_plot_data_availability():
    """
    Tests the plot_data_availability function to ensure it creates and saves the plot successfully.
    """

    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_data_availability(df, output_dir)
    assert (output_dir / f"data_availability_heatmap_{STARTDATE}.png").is_file()

def test_plot_max_contract_number():
    """
    Tests the plot_max_contract_number function to ensure it creates and saves the plot successfully.
    """

    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_max_contract_number(df, output_dir)
    assert (output_dir / f"maximum_contract_number_{STARTDATE}.png").is_file()

def test_plot_max_contract_availability():
    """
    Tests the plot_max_contract_availability function to ensure it creates and saves the plot successfully.
    """

    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    paa.plot_max_contract_availability(df, output_dir)
    assert (output_dir / f"max_contract_availability_{STARTDATE}.png").is_file()

def test_plot_rolling_volatility():
    """
    Tests the plot_rolling_volatility function to ensure it creates and saves the plot successfully based on specified rolling window and contract number.
    """
    
    df = lcd.load_data(DATA_DIR)
    df = dp.clean_process_data(start_date=config.STARTDATE_OLD, end_date=config.ENDDATE_OLD, data_dir=DATA_DIR)
    output_dir = Path(config.OUTPUT_DIR)
    rolling_window = 60  # Specify the rolling window for this test
    contract_num = 1  # Specify the contract number for this test
    paa.plot_rolling_volatility(df, output_dir, rolling_window=rolling_window, contract_num=contract_num)
    assert (output_dir / f"{rolling_window}_months_rolling_volatility_{STARTDATE}.png").is_file()

if __name__ == '__main__':
    pytest.main()

