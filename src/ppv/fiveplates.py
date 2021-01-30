"""
Interface objects for the five_plates repository
(https://github.com/sdss/five_plates) which creates the 
input files for the plate design code.


Field: 

Platerun: 

"""
from . import _fp_available
from .data import io
from .util import scalar_column, paths
from . import config
from .process import simulate_platedesign
from .parse_platedata import fp_plateplans
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import vstack, Column
from astropy.io import ascii
import os


# Getting plateruns

_description = io.load_fp_description()


# HARD CODING FOR NOW
# TODO update when consensus reached with Felipe and Kevin

_available = list(_description['OriginalName'])

#  Needs to be in same order as _available
_prefect_name = list(_description['FinalName'])

_fp_to_prefect_name = {fp_name : prefect_name for
                       prefect_name, fp_name in
                       zip(_prefect_name, _available)}

plateruns = list(_fp_available)
platedata_paths = [paths.fp_platedata(prun) for prun in plateruns]

_plateruns_with_platedata = [prun for prun, pd_path in zip(plateruns, platedata_paths)
                             if pd_path is not None]

# Get main plate-data, this is akin to platePlan.par
_main_platedata = fp_plateplans(_plateruns_with_platedata)


def replace_space(val):
    return val.replace(' ', '_')

# get possible plateruns

def available_plateruns():
    return sorted(list(_fp_available))


def get_program_names(cartons_table):
    """
    Returns program names with only string in parenthesis 
    """
    programs = [re.findall('\(([^)]+)', prog)[0]
                if ('(' in prog) else prog  for
                prog in cartons_table['program']]
    return programs

def carton_to_program(field, carton):
    return field._cartons_table.loc[carton]['program']

def carton_to_priority(field, carton, instrument):
    program = carton_to_program(field, carton)
    # instrument is 'boss' or 'apogee'
    program_str = f'{instrument}_SCI_{program}'
    return field._priority_order.loc[program_str]['order']


###  platedef parsing functions  ###

def plateInput_files(pldef_params):
    """
    Get ordered list of plateInput files given plate_definitio pararmeters.


    Parameters
    ----------
    pldef_params : dictionary
        Should likely be the output of io.fp_platedef_params()
    """
    return [pldef_params[f'plateInput{N+1}'] for
            N in range(pldef_params['nInput'])]

def parse_program_name_from_file(field, designID, plate_input_filename):
    """
    Given plateInput filename, get the full program name in the order file.
    """
    pre_ = f'targetlist_{field}_'
    suf_ = f'_{designID}.txt'
    return plate_input_filename.replace(pre_, '').replace(suf_, '')

def parse_instrument_name_from_file(field, designID, plate_input_filename):
    """
    Given plateInput filename, get the full program name in the order file.
    """
    pre_ = f'targetlist_{field}_'
    return plate_input_filename.replace(pre_, '').split('_')[0]

# CartonLists and defaultparameters files are per Platerun
# Let's cache this so they are only read one time

default_params = {}
cartons = {}


def get_defaultparams(platerun):
    try:
        return default_params[platerun]
    except KeyError:
        dparams = io.load_fp_defaultparams(platerun)
        default_params[platerun] = dparams
        return dparams

def get_cartons_table(platerun):
    dparams = get_defaultparams(platerun)
    list_version = dparams.loc['carton_list_version']['Value']
    try:
        return cartons[platerun]
    except KeyError:
        carton_table = io.load_fiveplates_cartons(platerun, list_version)
        carton_table['fp_program'] = get_program_names(carton_table)
        cartons[platerun] = carton_table
        return carton_table


class Field:
    """
    Class to act as interface to fields in the five_plates repository.

    The Field object will inspect the corresponding plateDefinition file
    in 'targetlists.zip'. 
    It will then find the list of input files, parse them, and create
    a table of targets with a new column for priority.
    The priority column reflects the ordered priority of programs
    coming from the fiberfilling modes (*order.txt files).

    To make the five_plates.Field as consistent as possible with
    groups.Field, the code treats the '_targets' and '_targets_clean'
    files as if they were plates.
    This should be completely transparent to the user.

    If a field has only ONE design, you need only specify the Field name.
    For fields with multiple designs (usually BHM), the design_id keyword
    must be specified.
    """

    def __init__(self, fieldname, design_id=None):
        """

        Parameters
        ----------
        fieldname : str
            field name. These can be found in the Platerun summary files
        designID : int
        """
        self.name = fieldname
        self.designID = design_id
        self._pd_indx = self._indx_in_platedata()
        self._pdata = _main_platedata[self._pd_indx] # row for field
        # Get designID if not specified, IF specified, just recopy
        self.designID = self._fetch_designID()
        self.epoch = self._get_epoch()
        self._radius = self._get_radius() * u.degree
        self.ra, self.dec = self._center()
        self.center = SkyCoord(self.ra * u.deg, self.dec * u.deg,
                               obstime=Time(self.epoch, format='decimalyear'))
        self.platerun = self._get_platerun()
        self._platedef_params = io.fp_platedef_params(self.platerun,
                                                      self.name,
                                                      self.designID)
        self._fiber_filling = self._get_filling_scheme()
        self._program_priorities = io.load_fiveplates_priority(self.platerun,
                                                               self._fiber_filling)

    def __repr__(self):
        return f'five_plates Field({self.name!r})'

    def __str__(self):
        first = f'five_plates Field: {self.name!r}, RA: {self.ra!r}, Dec: {self.dec!r}\n'
        second = f'platerun ID: {self.platerun!r}'
        return first + second

    def _indx_in_platedata(self):
        # initial index
        indx = _main_platedata.loc_indices[self.name]
        if isinstance(indx, list):  # multiple indices
            # better have DesignID then
            try:
                # Five plates MAY have multiple lines in plate_data that correspond
                # to EXACT SAME design. Need to be flexible here.
                indx = _main_platedata.loc_indices['designid', self.designID]
                if isinstance(indx, list):  # multiple lines, one design
                    indx = indx[0]
                return indx
            except TypeError:
                print('Field: {self.name!r} has multiple designs.')
                print('Design: {self.designID!r} not found.')
                print('Please construct Field object with correct designID.')
        else:  # only one row, yay
            return indx

    def _fetch_designID(self):
        return self._pdata['designid']

    def _get_epoch(self):
        return self._pdata['epoch']

    def _get_radius(self):
        return self._pdata['radius']

    def _get_filling_scheme(self):
        return self._pdata['fiberfilling']

    def _get_platerun(self):
        return self._pdata['platerun']

    def _center(self):
        ra = self._pdata['raCen']
        dec = self._pdata['decCen']
        return ra, dec

    def firstcarton_program_name(self, carton):
        return carton_to_program(self, carton)

    def _process_plateinput(self, targetlist_filename):
        targetlist_table = io.fp_plateinput(self.platerun, self.name,
                                            self.designID, targetlist_filename)
        priority_program_name = parse_program_name_from_file(self.name, self.designID,
                                                             targetlist_filename)
        instrument = parse_instrument_name_from_file(self.name, self.designID,
                                                     targetlist_filename)
        platerun_priority_N = self._program_priorities.loc[priority_program_name]['order']
        # add ID values to table
        Nrows = len(targetlist_table)
        targetlist_table.add_column(scalar_column(instrument, Nrows, 'instrument'))
        targetlist_table.add_column(scalar_column(platerun_priority_N,
                                                  Nrows, 'order_priority'))
        targetlist_table.add_column(scalar_column(priority_program_name, Nrows,
                                                  'order_name'))
        return targetlist_table

    def _full_plateinput_table(self):
        _plateinput_filenames = plateInput_files(self._platedef_params)
        # APOGEE standards made separately! ARRGGGHHH
        plinput_tables = [self._process_plateinput(targetlist_file) for
                          targetlist_file in _plateinput_filenames if
                          'apogee_STA' not in targetlist_file]
        full_table = vstack(plinput_tables)
        full_table.rename_column('Catalog_id', 'catalogid')
        full_table.sort('catalogid')
        full_table.add_column(scalar_column(self.name, len(full_table),
                                            'field'))
        full_table.add_column(scalar_column(self.designID, len(full_table),
                                            'designid'))
        return full_table

    @property
    def targets(self):  # Loads full plateInput table
        try:
            return self._plateinput
        except AttributeError:
            self._plateinput = self._full_plateinput_table()
            return self._plateinput

    @property
    def clean_targets(self):  # Loads targets_clean file
        try:
            return self._targets
        except AttributeError:
            self._targets = self._load_table('clean')
            return self._targets

    @property
    def available_targets(self):  # Loads targets.txt file
        try:
            return self._input_targets
        except AttributeError:
            self._input_targets = self._load_table('input')
            return self._input_targets

    @property
    def pseudo_plate(self):
        try:
            return self._pseudo_plate
        except AttributeError:
            self._pseudo_plate = self._sim_science_targs()
            return self._pseudo_plate

    def _sim_science_targs(self, random_seed=None):
        """
        Calls process.simulate_platedesign to create table of SCIENCE targets
        that will likey be/ will be assigned a fiber once through plate design.
        Starts with the targetlists table.

        Parameters
        ----------
        random_seed : int
            if None, default random seed in process.simulate_platedesign will
            be used.
        """
        nBOSS_science = self._platedef_params['nBOSS_science']
        nAPOGEE_science = self._platedef_params['nAPOGEE_science']

        if isinstance(random_seed, int):
            return simulate_platedesign(self.targets,
                                        nAPOGEE_science,
                                        nBOSS_science,
                                        random_seed=random_seed)
        else:
            return simulate_platedesign(self.targets,
                                        nAPOGEE_science,
                                        nBOSS_science)

    def _load_table(self, clean_or_input):
        """
        Takes all converts plates in field and combines target tables.
        Creates new column with the fieldname. While repititive, this will
        make Plateruns much easier to implement.

        clean_or_input: str
            contains 'clean' for targets_clean.
        """
        data = io.load_fiveplates_field(self.platerun,
                                        self.name,
                                        self.designID,
                                        type=clean_or_input)   # 'clean' OR 'input'
        data.rename_column('Catalog_id', 'catalogid')  # keep consistent with plates
        N_targets = len(data)
        field_column = Column(data=[self.name] * N_targets,
                              name='field',
                              dtype='S200')
        data.add_column(field_column)
        data.sort('catalogid')
        return data

    def _contains(self, catIDs):
        """
        Checks for membership in a plate based on catalogID.

        Parameters
        ----------
        catIDs : array-like
            List of catalogIDs.

        # TODO make util function that checks if catIDs is a scalar or array
        """
        try: # already array-like
            return np.in1d(self.targets['Catalog_id'], catIDs)
        except TypeError:
            return np.in1d(self.targets['Catalog_id'], np.array([catIDs]))

    def get_targets(self, catalogIDs):
        """
        Return rows of the Field targets table given a list of catalogIDs
        """
        return self.targets[self._contains(catalogIDs)]

    def contains(self, catIDs):
        """
        Checks for membership in a plate based on catalogID.
        ALL catIDs must be in plate to return True.

        Parameters
        ----------
        catIDs : array-like
            List of catalogIDs.

        """
        try: # already array-like
            return np.in1d(catIDs, self.targets['catalogid'])
        except TypeError:
            return np.in1d(np.array([catIDs]), self.targets['catalogid'])



class Platerun:
    """
    Class to act as interface to platerun in five_plates repository.
    """

    def __init__(self, run_name):
        if _check_platerun(run_name):
            pass  # all is well, platerun available
        self.name = run_name
        self.platedata = io.load_fp_platedata(run_name)
        self.fieldnames = self._get_fields()
        self.designIDs = self._get_designIDs()
        self._filling_modes = self._get_filling_modes()
        self._defaultparams = io.load_fp_defaultparams(run_name)
        self.fill_priorities = self._parse_fill_priorities()
        self._carton_list_version = self._defaultparams.loc['carton_list_version']['Value']
        self._cartons_table = io.load_fiveplates_cartons(self.name,
                                                         self._carton_list_version)

    def _get_fields(self):
        return list(self.platedata['fieldname'])

    def _get_designIDs(self):
        return list(self.platedata['designid'])

    def load_fields(self):
        return [Field(fieldname, design_id=designID) for fieldname, designID in
                zip(self.fieldnames, self.designIDs)]

    def _get_filling_modes(self):
        return list(set(self.platedata['fiberfilling']))

    def _parse_fill_priorities(self):
        """
        Construct dictionary of filling_modes to list of par
        """
        return {fill_mode: io.load_fiveplates_priority(self.name, fill_mode) for
                fill_mode in self._filling_modes}

    @property
    def fields(self):
        try:
            return self._fields
        except AttributeError:
            self._fields = self.load_fields()
            return self._fields

    @property
    def targets(self):
        try:
            return self._targets
        except AttributeError:
            print(f"""Please be patient.
                      Initial target loading can take up to 1 second per field.
                      Loading target data from {len(self.fieldnames)} Fields...""")
            self._targets = self._load_table()
            return self._targets

    def _load_table(self):
        """
        Takes all fields within platerun and combines target tables.
        """

        table = vstack([field.targets for field in self.fields])
        table.sort('catalogid')
        return table

    def _contains(self, catIDs):
        """
        Checks for membership in a plate based on catalogID.

        Parameters
        ----------
        catIDs : array-like
            List of catalogIDs.

        # TODO make util function that checks if catIDs is a scalar or array
        """
        try: # already array-like
            return np.in1d(self.targets['catalogid'], catIDs)
        except TypeError:
            return np.in1d(self.targets['catalogid'], np.array([catIDs]))

    def get_targets(self, catalogIDs):
        """
        Return rows of the Platerun targets table given a list of catalogIDs
        """
        return self.targets[self._contains(catalogIDs)]


class PlateRunMissingError(Exception):
    def __init__(self, run_name):
        if run_name:
            self.message = run_name
        else:
            self.message = None

    def __str__(self):
        if self.message:
            first = f'\nPlateRunMissingError, {self.message} is not an available platerun'
            second = f'\n ======================================================== \n'
            third = ' Make sure you cloned and pulled the latest five_plates commit!\n'
            third_half = ' AND update your ppv_setup.ini file!'
            fourth = f'\n ======================================================== \n'
            return first + second + third + third_half + fourth
            # return f'PlateRunMissingError, {self.message} is not an available platerun'
        else:
            return 'PlateRunMissingError has been raised'


def _check_platerun(run_name):
    if run_name in available_plateruns():
        return True     # All is well
    else:  # platerun NOT available
        raise PlateRunMissingError(run_name)





