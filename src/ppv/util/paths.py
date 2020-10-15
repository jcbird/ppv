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

#  five_plates
##############

def _five_plates_relpaths():
    tree_ =  os.walk(config.fiveplates_dir)
    dirs_ = [Path(root_dir) for (root_dir, _, _) in tree_]
    relpaths = [dir_.relative_to(config.fiveplates_dir) for dir_ in dirs_
                if dir_.name.endswith('m')]  # only keep in '(m)apper'
    return relpaths

def _five_plates_available_plateruns():
    relpaths = _five_plates_relpaths()
    return [relpath.name for relpath in relpaths]

def _map_fp_name_dir():
    """
    Make dictonary mapping name of the platerun to the directory
    under the hood. This absracts away 'first_drafts' directory from
    the user.
    """
    relpaths = _five_plates_relpaths()
    names = [relpath.name for relpath in relpaths]
    return {name: relpath for name, relpath in zip(names, relpaths)}

_fp_name_to_dir = _map_fp_name_dir()

def fiveplates_platerun(platerun):
    """
    gets directory of platerun in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    """
    return config.fiveplates_dir / _fp_name_to_dir[platerun]

def fiveplates_summary(platerun):
    """
    path to summary file in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    """
    summary_file = f'plate_data_{platerun}.txt'
    return fiveplates_platerun(platerun) / summary_file
    
def fiveplates_cartons(platerun):
    """
    path to cartons file in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    """
    # Flexible path finding due to e.g., 'cartons_list.v5.txt'
    files = os.listdir(fiveplates_platerun(platerun))
    cartons_file = list(filter(lambda X: 'cartons_list' in X, files))[0]
    return fiveplates_platerun(platerun) / cartons_file

def fiveplates_priority(platerun, filling_scheme):
    """
    path to cartons file in five_plates repo.


    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    filling_scheme : str
        FiberFilling column in fiveplates_cartons file, e.g., 'MWM_30min'
    """
    priority_file = f'{filling_scheme}_order.txt'
    return fiveplates_platerun(platerun) / priority_file
    

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
