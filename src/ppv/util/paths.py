"""
Utility module
"""
from .. import config
from pathlib import Path
import os


def platePlans_par():
    return config.plate_dir / 'platePlans.par'

def plate_plans():
    return config.plate_dir / 'platePlans_sdss5.fits'


def platenum_as_str(platenum):
    """String representation of platenumber with leading zeros if necessary.

    Parameters
    ----------
    platenum : int
        Number of plate

    Returns
    -------
    str
        String representation of plate number.
    """
    return '{:06d}'.format(platenum)


def plate_batch(platenum):
    """
    Given platenumber, get the path to the directory
    containing the platenum directory; e.g., '0150XX' given
    15020 as input.

    Parameters
    ----------
    platenum : str
        Number of plate (string to include leading zeros)
    """
    # Turns 15020 into '0150XX'
    batch_num = f'{platenum_as_str(platenum)[:-2]}XX'
    return config.plate_dir / batch_num


def plate(platenum):
    """Given platenumber, get the directory name containing
       the plate files.

    Parameters
    ----------
    platenum : str
        Number of plate (string to include leading zeros)

    """
    return plate_batch(platenum) / platenum_as_str(platenum)


def plateholes_file(platenum):
    """string representation of plateHoles files with correct formatting.

    Parameters
    ----------
    platenum :
        Number of plate (string to include leading zeros)
    """
    return 'plateHoles-{}.par'.format(platenum_as_str(platenum))

def plateholes(platenum):
    """gets path plateholes file.

    Parameters
    ----------
    platenum : str
        Number of plate (string to include leading zeros)
    """
    filename = plateholes_file(platenum)
    return plate(platenum) / filename
