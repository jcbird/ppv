"""
functions for loading (writing?) data from disk
"""
from ..util import paths, download
from .. import config
from astropy.table import Table
from astropy.io import ascii
from zipfile import ZipFile
import os
import numpy as np

# load yanny reader and writer (this works for platePlans.par)
# but it does not for the plugHoles files due to dtype issue.

from astropy.io.registry import (register_identifier, register_reader,
                                 register_writer)
from pydl.pydlutils.yanny import (is_yanny, read_table_yanny,
                                  write_table_yanny)
register_identifier('yanny', Table, is_yanny)
register_reader('yanny', Table, read_table_yanny)
register_writer('yanny', Table, write_table_yanny)

# END Yanny config


def _parse_plate_plans():
    """
    Prunes the platePlans.par file to only have SDSS-V plates AND
    converts parameter file to fits table for easy access.
    Only needs to be done when updating allplate_summary; e.g.,
    when a platerun is missing from ppv.available_plateruns.
    """
    platePlans = Table.read(os.fspath(paths.platePlans_par()), format='yanny',
                            tablename='PLATEPLANS')
    # Check for either mwm or bhm plate
    is_mwm_plate = np.array(['mwm' in prun for prun in platePlans['platerun']])
    is_bhm_plate = np.array(['bhm' in prun for prun in platePlans['platerun']])
    is_sdss5_plate = np.bitwise_or(is_mwm_plate, is_bhm_plate)

    sdss5_plates = platePlans[is_sdss5_plate]
    out_filename = paths.plate_plans()
    # delete the file if it exists
    if out_filename.exists():
        os.remove(os.fspath(out_filename))
    sdss5_plates.write(out_filename, overwrite='True', format='fits')
    print(f'SDSS-V platePlans table written to {out_filename}')
    return None


def load_plansummary():
    if not paths.plate_plans().exists():  # Need to download
        try:
            download.plate_plans()
            _parse_plate_plans()  # if parsing successful
        except:
            print(f'An error occurred. {os.fspath(paths.plate_plans())} does not exist\n')
            print(f'AND an error occured when trying to execute either\n')
            print(f'util.download.plate_plans OR _parse_plate_plans\n')
    else:
        _parse_plate_plans()  # already there, parse it
    return Table.read(os.fspath(paths.plate_plans()), format='fits')


# TODO Make summary file loading more flexible. ARRRGHHH!
def load_fiveplates_summary(platerun):
    """
    This is hard-coded for 2020.08.x.mwm-bhm!!! Need to make the file format
    machine-readable!
    """
    summary_file = paths.fiveplates_summary(platerun)
    if summary_file.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(summary_file))
    return ascii.read(os.fspath(summary_file), header_start=1,
                      format='commented_header')


def load_fiveplates_field(platerun, field_file_string):
    """
    path to zip file containing fields_files in five_plates repo.

    Parameters
    ----------
    platerun : str
        identifier of platerun, e.g. '2020.08.x.mwm-bhm'
    field_file_string : str
        typically the output of paths.fiveplates_clean_field_file OR
        paths.fiveplates_field_file 
    """
    fields_zip = paths.fiveplates_fieldfiles(platerun)

    with ZipFile(os.fspath(fields_zip)) as fp_zip:
        with fp_zip.open(field_file_string, 'r') as field:
            data = Table.read(field, format='ascii.commented_header')
    return data
