"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

import sys
sys.path.insert(1, "./src/")


import config
from pathlib import Path
from doit.tools import run_once
import platform
import subprocess
import os

import load_commodities_data
import data_preprocessing

OUTPUT_DIR = config.OUTPUT_DIR
DATA_DIR = config.DATA_DIR
INPUTFILE = config.INPUTFILE
LOADBACKPATH_CLEAN = config.LOADBACKPATH_CLEAN

# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Darwin":
        return "nix"
    elif os_name == "Linux":
        return "nix"
    else:
        return "unknown"


os_type = get_os()


def task_data_preprocessing():
    """Task to preprocess data"""

    #Check if Commodities_data.csv is available to load
    file_dep = [DATA_DIR/"manual"/INPUTFILE]
    
    #Check if Clean and Preprocessed Data is already available
    processed_files = [f for f in LOADBACKPATH_CLEAN.iterdir() if f.name.startswith("clean") and f.is_file()]
    target = [DATA_DIR / "manual" / file for file in processed_files]

    #Execute the following task
    action = ["python src/data_preprocessing.py"]
    
    #return stuff
    return{
        "actions":action,
        "file_dep":file_dep,
        "targets":target,
        "clean":True
        }

def task_replicate_results():
    """Task to replicate the results."""

    #Check if Clean Datasets are available to load
    processed_files = [f for f in LOADBACKPATH_CLEAN.iterdir() if f.name.startswith("clean") and f.is_file()]
    file_dep = [DATA_DIR / "manual" / file for file in processed_files]
    
    #Check if Output Tables are already Populated and Available
    output_files = [f for f in OUTPUT_DIR.iterdir() if f.name.startswith("Table") and f.is_file()]
    target = [OUTPUT_DIR/ file for file in output_files]

    #Execute the following task
    action = ["python src/replicate_results.py"]

    #return stuff
    return{
        "actions":action,
        "file_dep":file_dep,
        "targets":target,
        "clean":True
        }

def task_produce_tables_latex():
    """Task to replicate the results."""

    #Check if Clean Datasets are available to load
    processed_files = [f for f in LOADBACKPATH_CLEAN.iterdir() if f.name.startswith("clean") and f.is_file()]
    file_dep = [DATA_DIR / "manual" / file for file in processed_files]
    
    #Check if LaTex Tables are already Available
    output_files = [f for f in OUTPUT_DIR.iterdir() if f.name.startswith("Tex") and f.is_file()]
    target = [OUTPUT_DIR/ file for file in output_files]

    #Execute the following task
    action = ["python src/df_to_latex.py"]

    #return stuff
    return{
        "actions":action,
        "file_dep":file_dep,
        "targets":target,
        "clean":True
        }

def task_additional_analysis():
    """Task to perform additional analysis."""

    #Check if Commodities_data.csv is available to load
    file_dep = [DATA_DIR / "manual"/"clean_1970_2008_commodities_data.csv"]

    file_output = [
        "commodities_by_sector.png",
        "data_availability_heatmap.png",
        "maximum_contract_number.png",
        "max_contract_availability.png",
        "Aluminium_futures_contracts_time_series.png",
        "monthly_returns_distribution_contract_2.png",
        "monthly_returns_stats_contract_2.tex",
        "60_months_rolling_volatility.png",
        "60_months_rolling_sharpe_ratio.png",
        "Aluminium_contracts_1_2_basis.png"
    ]

    target = [OUTPUT_DIR / file for file in file_output]

    #Execute the following task
    action = ["python src/perform_additional_analysis.py"]

    #return stuff
    return{
        "actions":action,
        "file_dep":file_dep,
        "targets":target,
        "clean":True
        }

def task_compile_latex_docs():
    """Compile the LaTex documents to PDFs
    Outputs:
        PDFs in Reports
    """
    file_dep = [
        "./reports/report_simple_example.tex",
    ]

    file_output = [
         "./reports/report_simple_example.pdf"
    ]
    targets = [file for file in file_output]

    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/report_simple_example.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/report_simple_example.tex",  # Clean
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }