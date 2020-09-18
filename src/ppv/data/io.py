"""
functions for loading (writing?) data from disk
"""

from astropy.table import Table
from .. import config


def load_plansummary():
    return Table.read(config._plansummary, format='fits')



