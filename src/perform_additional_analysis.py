"""
This module contains functions for visualizing commodity data in various forms including
sector distribution, data availability, contract numbers, and time series analysis. It is
designed to assist in the analysis and presentation of commodities data by generating
informative plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
from scipy.stats import skew, kurtosis
from matplotlib.colors import ListedColormap

import warnings
warnings.filterwarnings("ignore")
import config
from pathlib import Path

import data_preprocessing as dp

DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE
OUTPUT_DIR = config.OUTPUT_DIR
STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD
LOADBACKPATH_CLEAN = config.LOADBACKPATH_CLEAN

#clean_data_file_path_1970 = Path(DATA_DIR) / "manual"/"clean_1970_2008_commodities_data.csv"
#df = pd.read_csv(clean_data_file_path_1970)

def plot_commodities_by_sector(df, OUTPUT_DIR, start_date = STARTDATE):
    '''
    This function plots the number of commodities in each sector and stores the plot as a .png file in the output directory.
    '''
    commodity_sector_mapping = {
        'Cocoa': 'Agriculture', 'Corn': 'Agriculture', 'Cotton': 'Agriculture', 'Live cattle': 'Livestock',
        'Oats': 'Agriculture', 'Orange juice': 'Agriculture', 'Soybean meal': 'Agriculture', 'Soybeans': 'Agriculture',
        'Wheat': 'Agriculture', 'Feeder cattle': 'Livestock', 'Coffee': 'Agriculture', 'Gold': 'Metals',
        'Silver': 'Metals', 'Canola': 'Agriculture', 'Crude Oil': 'Energy', 'Heating Oil': 'Energy',
        'Lean hogs': 'Livestock', 'Palladium': 'Metals', 'Platinum': 'Metals', 'Lumber': 'Agriculture',
        'Unleaded gas': 'Energy', 'Copper': 'Metals', 'Rough rice': 'Agriculture', 'Natural gas': 'Energy',
        'Aluminium': 'Metals', 'Gasoline': 'Energy',
    }

    # Map the commodities to sectors
    df['Sector'] = df['Commodity'].map(commodity_sector_mapping)

    # Create the plot
    plt.figure(figsize=(10, 5))
    df.groupby('Sector')['Commodity'].nunique().plot(kind='bar', title='Number of Commodities in Each Sector')
    plt.ylabel('Number of Commodities')
    plt.xlabel('Sector')

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"commodities_by_sector_{start_date}.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_data_availability(df, OUTPUT_DIR, start_date = STARTDATE):
    '''
    This function creates a heatmap showing the availability of data for each commodity across different contracts
    and saves the plot as a .png file in the output directory.
    '''
    # Create the pivot table
    pivot_df = df.pivot_table(index='Commodity', columns='Contract', values='ClosePrice', aggfunc='count')

    # Convert the counts to a binary format (1 for available, 0 for not available)
    availability_df = pivot_df.notnull().astype(int)
    cmap = ListedColormap(['#FFCCCB', '#ADD8E6'])  # Light red for unavailable, light blue for available

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(availability_df, cmap=cmap, cbar=False, linewidths=.5, annot=False)

    # Move the x-axis labels to the top
    ax = plt.gca()
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    plt.title('Data Availability Heatmap')
    plt.xlabel('Contract Number')
    plt.ylabel('Commodity')

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"data_availability_heatmap_{start_date}.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_max_contract_number(df, OUTPUT_DIR, start_date = STARTDATE):
    '''
    This function plots the maximum contract number available for each commodity and stores the plot as a .png file in the output directory.
    '''
    # Group by 'Commodity' and find the maximum 'Contract' number
    max_contract_df = df.groupby('Commodity')['Contract'].max()

    # Create the bar plot
    plt.figure(figsize=(10, 5))
    max_contract_df.plot(kind='bar', title='Maximum Contract # for each Commodity')
    plt.ylabel('Maximum Contract #')
    
    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"maximum_contract_number_{start_date}.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_max_contract_availability(df, OUTPUT_DIR, start_date = STARTDATE):
    '''
    This function creates a grid of plots showing the maximum contract availability at month-end for each commodity
    and stores the figure as a .png file in the output directory.
    '''

    if 'Date' in df.columns and not isinstance(df.index, pd.DatetimeIndex):
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime
        df.set_index('Date', inplace=True)  # Set 'Date' column as the index

    # Group by 'Commodity', resample to month-end, and find the maximum contract number
    sample_df_grouped = df.groupby('Commodity').resample('M').max()
    sample_df_grouped = sample_df_grouped.drop(columns='Commodity').reset_index()

    commodities = df['Commodity'].unique()
    num_commodities = df['Commodity'].nunique()

    # Determine the number of rows and columns for the subplots
    cols = 3
    rows = -(-num_commodities // cols)  # Ceiling division to ensure enough rows

    # Create a grid of subplots
    fig, axs = plt.subplots(rows, cols, figsize=(15, 3 * rows), sharex=True, sharey=True)
    fig.suptitle('Maximum Contract Availability at Month-End for Each Commodity', fontsize=16, y=1.02)
    axs = axs.flatten()

    # Plot the data for each commodity
    for idx, commodity in enumerate(commodities):
        if idx >= len(axs):
            break
        ax = axs[idx]
        data = sample_df_grouped[sample_df_grouped['Commodity'] == commodity]
        ax.plot(data['Date'], data['Contract'], linestyle='-')
        ax.set_title(commodity)
        ax.tick_params(axis='x', rotation=45)  # Rotating x-ticks for clarity
        ax.grid(True)

    # Hide any unused subplots
    for ax in axs[idx + 1:]:
        ax.set_visible(False)

    plt.tight_layout()

    # Save the figure
    file_path = Path(OUTPUT_DIR) / f"max_contract_availability_{start_date}.png"
    fig.savefig(file_path)
    plt.close()

def plot_rolling_volatility(df, OUTPUT_DIR, rolling_window=60, contract_num=2, start_date=STARTDATE):
    '''
    This function creates a plot showing the 5-year rolling volatility (annualized) and stores the plot as a .png file in the output directory.
    '''
    # Calculate the 5-year rolling volatility (annualized)
    returns_df = df[df['Contract'] == contract_num].resample('M').last()
    returns_df['Monthly returns'] = returns_df['ClosePrice'].pct_change()
    returns_df = returns_df.dropna()
    
    returns_df['Rolling Volatility'] = returns_df['Monthly returns'].rolling(window=rolling_window).std() * np.sqrt(12)

    # Create the plot
    plt.figure(figsize=(12, 6))
    returns_df['Rolling Volatility'].plot(title=f'{rolling_window} Months Rolling Volatility')
    plt.xlabel('Date')
    plt.ylabel('Rolling Volatility')

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"{rolling_window}_months_rolling_volatility_{start_date}.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_rolling_sharpe_ratio(df, OUTPUT_DIR, rolling_window=60, contract_num =2, start_date = STARTDATE):
    '''
    This function creates a plot showing the rolling Sharpe ratio and stores the plot as a .png file in the output directory.
    '''
    # Calculate the rolling mean returns (annualized) and the rolling Sharpe ratio
    returns_df = df[df['Contract'] == contract_num].resample('M').last()
    returns_df['Monthly returns'] = returns_df['ClosePrice'].pct_change()
    returns_df = returns_df.dropna()
    
    returns_df['Rolling Volatility'] = returns_df['Monthly returns'].rolling(window=rolling_window).std() * np.sqrt(12)
    returns_df['Rolling Mean Returns'] = returns_df['Monthly returns'].rolling(window=rolling_window).mean() * 12
    returns_df['Rolling Sharpe Ratio'] = returns_df['Rolling Mean Returns'] / returns_df['Rolling Volatility']

    # Create the plot
    plt.figure(figsize=(12, 6))
    returns_df['Rolling Sharpe Ratio'].plot(title=f'{rolling_window} Months Rolling Sharpe Ratio')
    plt.xlabel('Date')
    plt.ylabel('Rolling Sharpe Ratio')

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"{rolling_window}_months_rolling_sharpe_ratio_{start_date}.png"
    plt.savefig(file_path)
    plt.close()


if __name__ == '__main__':
    start_dates = [config.STARTDATE_OLD, config.STARTDATE_NEW]
    end_dates = [config.ENDDATE_OLD, config.ENDDATE_NEW]

    for start_date, end_date in zip(start_dates, end_dates):

        clean_data_file_path = Path(DATA_DIR) / "manual" / f"clean_{start_date[:4]}_{end_date[:4]}_{INPUTFILE}"
        df = pd.read_csv(clean_data_file_path)

        plot_commodities_by_sector(df, OUTPUT_DIR, start_date)
        plot_data_availability(df, OUTPUT_DIR, start_date)
        plot_max_contract_number(df, OUTPUT_DIR, start_date)
        plot_max_contract_availability(df, OUTPUT_DIR, start_date)
        plot_rolling_volatility(df, OUTPUT_DIR, rolling_window=60, contract_num=2, start_date=start_date)
        plot_rolling_sharpe_ratio(df, OUTPUT_DIR, rolling_window=60, contract_num=2, start_date=start_date)