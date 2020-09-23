"""
Parameter configuration
"""
from configparser import ConfigParser
from pathlib import Path

## Fixed relative path
_plansummary = Path(__file__).parent / 'data/platePlans_sdss5.fits'
##

## Configuration
config = ConfigParser()
config.read('setup.ini')

plate_dir = Path(config['paths']['plate_dir'])
## end Configuration



