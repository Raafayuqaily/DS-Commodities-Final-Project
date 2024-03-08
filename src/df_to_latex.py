# This python file is designed to convert a pandas dataframe into a latex file


from pathlib import Path
import logging
import config
import replicate_results
import load_commodities_data
import data_preprocessing

df = pd.DataFrame()
latex_table_string = df.to_latex(float_format=float_format_func)
print(latex_table_string)

path = OUTPUT_DIR / f'pandas_to_latex_simple_table1.tex'
with open(path, "w") as text_file:
    text_file.write(latex_table_string)