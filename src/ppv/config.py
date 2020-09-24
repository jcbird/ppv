"""
Parameter configuration
"""
from configparser import ConfigParser
from pathlib import Path
import os
import sys

## Fixed relative path
_plansummary = Path(__file__).parent / 'data/platePlans_sdss5.fits'
##


## Configuration
_config_path = Path.home() / '.config' / 'ppv_setup.ini'
_filename = _config_path.name
config = ConfigParser()

try:
    config.read_file(open(os.fspath(_config_path), 'r'))
    plate_dir = Path(config['paths']['plate_dir'])
except FileNotFoundError:
    print(f'Configuration file does not exist!')
    print(f'Copy {_filename} from the ppv repository to the directory {_config_path.parent}')
    print(f'AND edit the configuration file before proceeding')

## end Configuration



