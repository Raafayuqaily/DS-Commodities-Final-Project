"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based
"""

import sys
sys.path.insert(1, "./src/")


import config
from pathlib import Path
from doit.tools import run_once
import platform

import load_commodities_data
import data_preprocessing

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)

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


def copy_notebook_to_folder(notebook_stem, origin_folder, destination_folder):
    origin_path = Path(origin_folder) / f"{notebook_stem}.ipynb"
    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / f"_{notebook_stem}.ipynb"
    if os_type == "nix":
        command = f"cp {origin_path} {destination_path}"
    else:
        command = f"copy  {origin_path} {destination_path}"
    return command


def task_load_commodities_data():
    """Task to load commodities data"""
    file_dep = ["./src/load_commodities_data.py"]
    file_output = ["commodities_data.csv"]
    targets = [DATA_DIR / "manual" / file for file in file_output]

    return {
        "actions": [
            (load_commodities_data.load_data, [], {
                "data_dir": DATA_DIR,
                "file_name": "commodities_data.csv"
            }),
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

def task_data_preprocessing():
    """Task to preprocess data"""
    file_dep = ["./src/data_preprocessing.py", "./src/load_commodities_data.py"]
    file_output = ["preprocessed_data.csv"]
    targets = [DATA_DIR / "processed" / file for file in file_output]

    return {
        "actions": [
            (data_preprocessing.preprocess_data, [], {
                "df": load_commodities_data.load_data(data_dir=DATA_DIR, file_name="commodities_data.csv")
            }),
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_summary_stats():
    """ """
    file_dep = ["./src/example_table.py"]
    file_output = [
        "example_table.tex",
        "pandas_to_latex_simple_table1.tex",
    ]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/example_table.py",
            "ipython ./src/pandas_to_latex_demo.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_example_plot():
    """Example plots"""
    file_dep = [Path("./src") / file for file in ["example_plot.py", "load_fred.py"]]
    file_output = ["example_plot.png"]
    targets = [OUTPUT_DIR / file for file in file_output]

    return {
        "actions": [
            "ipython ./src/example_plot.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    notebooks = [
        "01_example_notebook.ipynb",
        "02_interactive_plot_example.ipynb",
    ]
    stems = [notebook.split(".")[0] for notebook in notebooks]

    file_dep = [
        # 'load_other_data.py',
        *[Path(OUTPUT_DIR) / f"_{stem}.py" for stem in stems],
    ]

    targets = [
        ## 01_example_notebook.ipynb output
        OUTPUT_DIR / "sine_graph.png",
        ## Notebooks converted to HTML
        *[OUTPUT_DIR / f"{stem}.html" for stem in stems],
    ]

    actions = [
        *[jupyter_execute_notebook(notebook) for notebook in stems],
        *[jupyter_to_html(notebook) for notebook in stems],
        *[copy_notebook_to_folder(notebook, Path("./src"), "./docs/_notebook_build/") for notebook in stems],
        *[jupyter_clear_output(notebook) for notebook in stems],
        # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
    ]
    return {
        "actions": actions,
        "targets": targets,
        "task_dep": [],
        "file_dep": file_dep,
        "clean": True,
    }




def task_compile_latex_docs():
    """Compile the LaTeX documents to PDFs"""
    file_dep = [
        "./reports/report_example.tex",
        "./reports/slides_example.tex",
        "./src/example_plot.py",
        "./src/example_table.py",
    ]
    file_output = [
        "./reports/report_example.pdf",
        "./reports/slides_example.pdf",
    ]
    targets = [file for file in file_output]

    return {
        "actions": [
            "latexmk -xelatex -cd ./reports/report_example.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/report_example.tex",  # Clean
            "latexmk -xelatex -cd ./reports/slides_example.tex",  # Compile
            "latexmk -xelatex -c -cd ./reports/slides_example.tex",  # Clean
            # "latexmk -CA -cd ../reports/",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""
    file_dep = [
        "./docs/conf.py",
        "./docs/index.rst",
        "./docs/myst_markdown_demos.md",
        "./docs/api.rst",
    ]
    targets = [
        "./docs/_build/html/index.html",
        "./docs/_build/html/myst_markdown_demos.html",
        "./docs/_build/html/api.html",
    ]

    return {
        "actions": ["sphinx-build -M html ./docs/ ./docs/_build"],
        "targets": targets,
        "file_dep": file_dep,
        "task_dep": ["run_notebooks"],
        "clean": True,
    }
