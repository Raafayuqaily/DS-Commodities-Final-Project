"""
Load project configurations from .env files.
Provides easy access to paths and credentials used in the project.
Meant to be used as an imported module.

If `config.py` is run on its own, it will create the appropriate
directories.

For information about the rationale behind decouple and this module,
see https://pypi.org/project/python-decouple/

Note that decouple mentions that it will help to ensure that
the project has "only one configuration module to rule all your instances."
This is achieved by putting all the configuration into the `.env` file.
You can have different sets of variables for difference instances, 
such as `.env.development` or `.env.production`. You would only
need to copy over the settings from one into `.env` to switch
over to the other configuration, for example.
"""

from decouple import config
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (BASE_DIR / config('DATA_DIR', default=Path('data'), cast=Path)).resolve()
OUTPUT_DIR = (BASE_DIR / config('OUTPUT_DIR', default=Path('output'), cast=Path)).resolve()
REPORTS_DIR = (BASE_DIR / config('REPORTS_DIR', default=Path('reports'), cast=Path)).resolve()
LOADBACKPATH_CLEAN = Path(DATA_DIR / "manual")

INPUTFILE = 'commodities_data.csv'

STARTDATE_OLD = '1970-01-01'
ENDDATE_OLD = '2008-12-31'

STARTDATE_NEW = '2009-01-01'
ENDDATE_NEW = '2024-12-31'

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
