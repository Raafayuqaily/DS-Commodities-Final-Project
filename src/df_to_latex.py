# This python file is designed to convert a pandas dataframe into a latex file

from pathlib import Path
import pandas as pd
import logging
import config
import replicate_results  
logging.basicConfig(level=logging.INFO)


OUTPUT_DIR = Path(config.OUTPUT_DIR)

def generate_latex_table():
    
    try:
        
        metrics_df_final = replicate_results.combine_metrics(pre_processed_df)
        
        # Convert the DataFrame to a LaTeX string
        latex_table_string = metrics_df_final.to_latex(index=True, float_format="%.2f")

        # Print the LaTeX string to console (helpful for debugging)
        print(latex_table_string)

        # Write the LaTeX string to a file in the OUTPUT_DIR
        output_file_path = OUTPUT_DIR / 'metrics_df_final_table.tex'
        with open(output_file_path, "w") as text_file:
            text_file.write(latex_table_string)
        logging.info(f"Table saved to {output_file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":menmma
    
    generate_latex_table()
