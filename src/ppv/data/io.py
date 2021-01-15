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


def _load_commented_header(file_path, **table_kwds):
    if file_path.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(file_path))
    return  Table.read(os.fspath(file_path),
                       format='ascii.commented_header',
                       **table_kwds)


def load_fp_description():
    colnames = ['OriginalName', 'Nplates_o',
                'FinalName', 'Nplates_f',
                'CurrName', 'NeededBy',
                'Notes', 'Cartonlist', 'Scripts_Date']
    return _load_commented_header(paths.fiveplates_description(),
                                  names=colnames)


_pd_2020_08_x_colnames = ['fieldname',
                          'version',
                          'plateid',
                          'designid',
                          'locationid',
                          'raCen',
                          'decCen',
                          'epoch',
                          'radius',
                          'ha',
                          'fiberfilling',
                          'priority',
                          'platerun',
                          'notes']

_pd_standard_colnames = ['fieldname',
                  'plateid',
                  'designid',
                  'locationid',
                  'raCen',
                  'decCen',
                  'epoch',
                  'radius',
                  'ha',
                  'cadencecategory',
                  'priority',
                  'fiberfilling',
                  'Nsky_APOGEE',
                  'Nstd_APOGEE',
                  'Nsky_BOSS',
                  'Nstd_BOSS']

def load_fp_platedata(platerun, **table_kwds):
    """
    table format for platedata has changed a lot from run to run.
    Hoping to standardize. For now, this is a little hacky and fragile
    if five_plates makes further changes.
    """
    pd_table = _load_commented_header(paths.fp_platedata(platerun))

    if platerun == '2020.08.x.bhm-mwm':  # different table colnames
        pd_table.rename_columns(pd_table.colnames, _pd_2020_08_x_colnames)
    else:
        # check if 'platerun' column exists
        pd_colnames_lower = [col.lower() for col in pd_table.colnames]
        if 'platerun' in pd_colnames_lower:
            pd_table.rename_columns(pd_table.colnames, _pd_standard_colnames + ['platerun'])
        else:   # need to add platerun
            pd_table.rename_columns(pd_table.colnames, _pd_standard_colnames + ['notes'])
            Nrows = len(pd_table)
            pd_table['platerun'] = [platerun] * Nrows
    return pd_table


def load_fp_defaultparams(platerun):
    params_file = paths.fp_defaultparams(platerun)
    if params_file.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(params_file))
    dp_table =  Table.read(os.fspath(params_file), format='ascii.commented_header')
    dp_table.add_index('Parameter')
    return dp_table

def load_fiveplates_summary(platerun):
    """
    """
    summary_file = paths.fiveplates_summary(platerun)
    if summary_file.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(summary_file))
    return Table.read(os.fspath(summary_file), format='ascii')

def load_fiveplates_cartons(platerun, version):
    """
    """
    cartons_file = paths.fiveplates_cartons(platerun, version=version)
    if cartons_file.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(cartons_file))
    cartons_table = Table.read(os.fspath(cartons_file), format='ascii')
    cartons_table.add_index('carton')
    return cartons_table

def load_fiveplates_priority(platerun, filling_scheme):
    """
    """
    priority_file = paths.fiveplates_priority(platerun, filling_scheme)
    if priority_file.exists():
        pass
    else:
        raise FileNotFoundError(os.fspath(priority_file))
    priority_table = Table.read(os.fspath(priority_file),
                                format='ascii.no_header')
    old_colname = priority_table.colnames[0]
    priority_indx = list(range(len(priority_table)))
    priority_table['order'] = priority_indx
    priority_table.rename_column(old_colname, 'program')
    priority_table.add_index('program')
    return priority_table

def load_fiveplates_field(platerun, field, designID, type='clean'):
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
    if paths.fiveplates_designfiles(platerun).exists():
        field_zip = paths.fiveplates_designfiles(platerun)
        if type=='clean':
            field_file_str = paths.fiveplates_clean_design_file(field, designID)
        else:
            field_file_str = paths.fiveplates_design_file(field, designID) # 'input'
    else:  # platerun before the switch to designfiles zip
        field_zip = paths.fiveplates_fieldfiles(platerun)
        if type=='clean':
            field_file_str = paths.fiveplates_clean_field_file(field)
        else:
            field_file_str = paths.fiveplates_field_file(field) # 'input'
    with ZipFile(os.fspath(field_zip)) as fp_zip:
        with fp_zip.open(field_file_str, 'r') as field:
            data = Table.read(field, format='ascii.commented_header')
    return data

def is_comment(s):
    return s.startswith('#')

def str_to_number_if_number(s):
    try:
        return int(s) if float(s) == int(float(s)) else float(s)
    except ValueError:  #  it's a string
        return s

def fp_platedef_params(platerun, field, designID):
    targetlists_zip = paths.fiveplates_targetlists(platerun)
    params = {}
    with ZipFile(os.fspath(targetlists_zip)) as tl_zip:
        with tl_zip.open(paths.fiveplates_platedef(field, designID), 'r') as pldef:
            rows = pldef.readlines()
            for row in rows:
                row = row.decode() # ZipFile must put this in bytes
                items_ = row.strip().split() # split on whitespace
                if row.startswith('#') or len(items_) < 2:
                    continue
                key = items_[0]
                if len(items_) == 2:   # simple key:value pair
                    value = str_to_number_if_number(items_[1])
                else: # it's a list
                    value = items_[1:]
                    value = [str_to_number_if_number(val) for val in value]
                params[key] = value
    return params

def fp_plateinput(platerun, field, designID, inputfile):
    targetlists_zip = paths.fiveplates_targetlists(platerun)
    with ZipFile(os.fspath(targetlists_zip)) as tl_zip:
        pl_input_path_str = f'{paths.fp_field_designID_dir(field, designID)}/{inputfile}'
        with tl_zip.open(pl_input_path_str, 'r') as pl_input:
            data = Table.read(pl_input, format='ascii.commented_header')
    return data
