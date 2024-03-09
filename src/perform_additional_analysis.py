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

clean_data_file_path = Path(DATA_DIR) / "manual"/"clean_1970_2008_commodities_data.csv"
df = pd.read_csv(clean_data_file_path)

def plot_commodities_by_sector(df, OUTPUT_DIR):
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
    file_path = Path(OUTPUT_DIR) / "commodities_by_sector.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_data_availability(df, OUTPUT_DIR):
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
    file_path = Path(OUTPUT_DIR) / "data_availability_heatmap.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_max_contract_number(df, OUTPUT_DIR):
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
    file_path = Path(OUTPUT_DIR) / "maximum_contract_number.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_max_contract_availability(df, OUTPUT_DIR):
    '''
    This function creates a grid of plots showing the maximum contract availability at month-end for each commodity
    and stores the figure as a .png file in the output directory.
    '''
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
    file_path = Path(OUTPUT_DIR) / "max_contract_availability.png"
    fig.savefig(file_path)
    plt.close()
    
def plot_commodity_time_series(df, OUTPUT_DIR, commodity = 'Aluminium'):
    '''
    This function creates a time series plot for the specified commodity's futures contracts
    and stores the plot as a .png file in the output directory.
    '''
    # Filter the DataFrame for the selected commodity
    
    df_select = df[df['Commodity'] == commodity]
    unique_contracts = df_select['Contract'].unique()

    # Create the time series plot
    plt.figure(figsize=(14, 7))
    for contract in unique_contracts:
        contract_data = df_select[df_select['Contract'] == contract]
        plt.plot(contract_data.index, contract_data['ClosePrice'], label=f'Contract {contract}')

    plt.yscale('log')
    plt.title(f'{commodity} Futures Contracts Time Series')
    plt.xlabel('Date')
    plt.ylabel('Close Price (log scale)')
    plt.legend()

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"{commodity}_futures_contracts_time_series.png"
    plt.savefig(file_path)
    plt.close()
     

def plot_return_distribution_and_save_formatted_stats(df, OUTPUT_DIR, contract_num = 2):
    '''
    This function creates a histogram plot showing the distribution of monthly returns for a specific contract,
    stores the plot as a .png file, and saves the formatted descriptive statistics in a LaTeX-formatted table.
    '''
    
    # Prepare the returns DataFrame
    
    returns_df = df[df['Contract'] == contract_num].resample('M').last()
    returns_df['Monthly returns'] = returns_df['ClosePrice'].pct_change()
    returns_df = returns_df.dropna()

    # Plotting the distribution of monthly returns with a histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(returns_df['Monthly returns'], kde=True, bins=30)
    plt.title(f'Distribution of Monthly Returns for Contract {contract_num}')
    plt.xlabel('Monthly Returns')
    plt.ylabel('Frequency')
    
    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"monthly_returns_distribution_contract_{contract_num}.png"
    plt.savefig(file_path)
    plt.close()

    # Calculating descriptive statistics
    stats = returns_df['Monthly returns'].describe()
    stats['skew'] = skew(returns_df['Monthly returns'])
    stats['kurtosis'] = kurtosis(returns_df['Monthly returns'])

    def format_stats(stats):
        stats['count'] = stats['count'].astype(int)
        for key in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']:
            stats[key] = stats[key].apply(lambda x: f"{x:.2%}")
        for key in ['skew', 'kurtosis']:
            stats[key] = stats[key].apply(lambda x: f"{x:.2f}")
        return stats
    
    # Format the stats
    formatted_stats = format_stats(stats)

    # Convert the stats to a DataFrame for easier LaTeX export
    stats_df = pd.DataFrame(formatted_stats).transpose()

    # Save the descriptive statistics as a LaTeX table
    stats_file_path = Path(OUTPUT_DIR) / f"monthly_returns_stats_contract_{contract_num}.tex"
    with open(stats_file_path, 'w') as f:
        f.write(stats_df.to_latex(escape=False))

def plot_rolling_volatility(df, OUTPUT_DIR, rolling_window=60, contract_num=2):
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
    file_path = Path(OUTPUT_DIR) / f"{rolling_window}_months_rolling_volatility.png"
    plt.savefig(file_path)
    plt.close()
    
def plot_rolling_sharpe_ratio(df, OUTPUT_DIR, rolling_window=60, contract_num =2):
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
    file_path = Path(OUTPUT_DIR) / f"{rolling_window}_months_rolling_sharpe_ratio.png"
    plt.savefig(file_path)
    plt.close()

def plot_basis_with_contracts(df, first_contract_num, last_contract_num,  OUTPUT_DIR, commodity= 'Aluminium'):
    '''
    This function calculates the basis, plots it along with the first and last contract prices for the specified commodity,
    and stores the plot as a .png file in the output directory.
    '''
    df_select = df[df['Commodity'] == commodity]
    unique_contracts = df_select['Contract'].unique()
    first_contract_num = unique_contracts[0]
    last_contract_num = unique_contracts[-1]
    
    # Filter the DataFrame for the first and last contracts
    contract1_df = df[df['Contract'] == first_contract_num]
    contract12_df = df[df['Contract'] == last_contract_num]

    # Merge the two contract DataFrames
    merged_df = pd.merge(contract1_df['ClosePrice'], contract12_df['ClosePrice'], left_index=True, right_index=True, suffixes=('_first', '_last')).ffill()

    # Calculate the basis
    merged_df = merged_df.resample('M').last()
    merged_df['Basis'] = ((np.log(merged_df['ClosePrice_first']) - np.log(merged_df['ClosePrice_last'])) / (last_contract_num - first_contract_num)) * 100

    # Set up the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(merged_df.index, merged_df['ClosePrice_first'], label=f'Contract {first_contract_num}', color='blue')
    ax1.plot(merged_df.index, merged_df['ClosePrice_last'], label=f'Contract {last_contract_num}', color='orange')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price', color='black')

    # Create a second y-axis for the basis
    ax2 = ax1.twinx()
    ax2.plot(merged_df.index, merged_df['Basis'], label='Basis', color='grey')
    ax2.set_ylabel('Basis (%)', color='grey')
    ax2.fill_between(merged_df.index, 0, merged_df['Basis'], color='grey', alpha=0.2)

    # Add titles and legend
    plt.title(f'{commodity} Contracts {first_contract_num} and {last_contract_num} with Basis Over Time')
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    # Save the plot
    file_path = Path(OUTPUT_DIR) / f"{commodity}_contracts_{first_contract_num}_{last_contract_num}_basis.png"
    plt.savefig(file_path)
    plt.close()


if __name__ == '__main__':
    com_sec = plot_commodities_by_sector(df, OUTPUT_DIR)