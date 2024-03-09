# This python file is designed to convert a pandas dataframe into a latex file

from pathlib import Path
import pandas as pd
import logging
import config
import replicate_results  
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(message)s')


OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE

def generate_latex_table(metrics_df_final, output_table_name):

    try:
        # Convert the DataFrame to a LaTeX string
        latex_table_string = metrics_df_final.to_latex(index=True, float_format="%.2f")

        # Write the LaTeX string to a file in the OUTPUT_DIR
        output_file_path = OUTPUT_DIR / f'{output_table_name}.tex'
        
        with open(output_file_path, "w") as text_file:
            text_file.write(latex_table_string)
        
        logging.info(f"LaTex for {output_table_name} Successfully Saved!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":

    start_dates = [config.STARTDATE_OLD[:4], config.STARTDATE_NEW[:4]]
    end_dates = [config.ENDDATE_OLD[:4], config.ENDDATE_NEW[:4]]
    
    for start_, end_ in zip(start_dates, end_dates):
        clean_data_file_path = Path(DATA_DIR) / "manual"/f"clean_{start_}_{end_}_{INPUTFILE}"
        clean_data_df = pd.read_csv(clean_data_file_path)
        combined_metrics_df_txt = replicate_results.combine_metrics(clean_data_df)
        output_table_name = f"Table1__{start_}_{end_}"
        generate_latex_table(combined_metrics_df_txt, output_table_name)
