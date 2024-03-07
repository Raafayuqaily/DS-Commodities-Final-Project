import pandas as pd
import config
from pathlib import Path

DATA_DIR = Path(config.DATA_DIR)

def load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv"):
    """
    Load commodities data csv, stored in /data/manual
    Setting the index of the dataframe to Date
    Returning the dataframe
    """
    file_path = Path(data_dir) / "manual" / file_name
    df = pd.read_csv(file_path)
    return df

def demo():
    """
    Creating an execution function for load_data
    that prints the first 5 rows of the dataframe
    """
    df = load_data()
    print(df.head())

if __name__ == "_main_":
    demo()



