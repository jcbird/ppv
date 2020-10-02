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

def fiveplates_platerun(platerun):
    """
    gets directory of platerun in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    
    """
    return config.fiveplates_dir / platerun

def fiveplates_summary(platerun):
    """
    path to summary file in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    """
    summary_file = f'{platerun}.summary'
    return fiveplates_platerun(platerun) / summary_file

def fiveplates_fieldfiles(platerun):
    """
    path to zip file containing fields_files in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    """
    field_files = f'{platerun}_field_files.zip'
    return fiveplates_platerun(platerun) / field_files

def fiveplates_clean_field_file(field):
    """
    string representation of targets_clean file for field within
    fiveplates_field_files zip file.

    Parameters
    ----------
    field : str
        identifier of field, e.g. 'GG_010'
    """
    return f'{field}_targets_clean.txt'

def fiveplates_field_file(field):
    """
    string representation of targets.txt file for field within
    fiveplates_field_files zip file.

    Parameters
    ----------
    field : str
        identifier of field, e.g. 'GG_010'
    """
    return f'{field}_targets.txt'
