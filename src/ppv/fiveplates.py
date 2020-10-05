"""
Interface objects for the five_plates repository
(https://github.com/sdss/five_plates) which creates the 
input files for the plate design code.


Field: 

Platerun: 

"""
from . import ppv
from .data import io
from .util import paths
from . import config
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import vstack, Column
from astropy.io import ascii
import os



# get possible plateruns

def available_plateruns():
    return os.listdir(config.fiveplates_dir)

# TODO could abstract this by getting names of columns for each class
# e.g., RAcol = 'RA(deg)', etc.

class Field:
    """
    Class to act as interface to fields in the five_plates repository.

    By default, Field will load the corresponding '_targets_clean.txt' files.
    Examination of '_targets.txt' file is forthcoming.

    To make the five_plates.Field as consistent as possible with
    groups.Field, the code treats the '_targets' and '_targets_clean'
    files as if they were plates.
    This should be completely transparent to the user.

    Platerun needs to be established first for five_plates because
    there is no overall summary file such as PlatePlans.par
    """

    def __init__(self, fieldname, platerun_name):
        """

        Parameters
        ----------
        fieldname : str
            field name. These can be found in the Platerun summary files
        platerun_name : str
            string identifier of platerun where the field is found; e.g. '2020.08.x.bhm-mwm'.
        """
        self.name = fieldname
        self.platerun_name = platerun_name
        # Need to load platerun summary 
        self.platerun_summary = io.load_fiveplates_summary(platerun_name)
        self._summary_indx = self._indx_in_platerun()
        self.epoch = self._get_epoch()
        # self._platenums = plates_of_field(self.name)
        # self._summary_indx = indx_in_plateruns(self.name)
        self.ra, self.dec = self._center()
        self.center = SkyCoord(self.ra * u.deg, self.dec * u.deg,
                               obstime=Time(self.epoch, format='decimalyear'))
        # TODO check epoch of field designation
        # self.platerun, self.programname = self.meta()
        self._radius = 1.49 * u.degree
        # Only ONE targets file per field as of now
        # can load when needed for now
        self._colnames = {'catalogid': 'Catalog_id'}

    def __repr__(self):
        return f'five_plates Field({self.name!r})'

    def __str__(self):
        first = f'five_plates Field: {self.name!r}, RA: {self.ra!r}, Dec: {self.dec!r}\n'
        second = f'platerun ID: {self.platerun_name!r}'
        return first + second

    def _indx_in_platerun(self):
        return np.where(self.platerun_summary['FieldName'] == self.name)[0]

    def _get_epoch(self):
        return self.platerun_summary['Epoch(yr)'][self._summary_indx]

    def _center(self):
        ra = self.platerun_summary['RA(deg)'][self._summary_indx][0]
        dec = self.platerun_summary['Dec(deg)'][self._summary_indx][0]
        return ra, dec


    @property
    def targets(self):  # Loads targets_clean file
        try:
            return self._targets
        except AttributeError:
            self._targets = self._load_table('clean')
            return self._targets

    @property
    def input_targets(self):  # Loads targets.txt file
        try:
            return self._input_targets
        except AttributeError:
            self._input_targets = self._load_table('input')
            return self._input_targets

    def _load_table(self, clean_or_input):
        """
        Takes all converts plates in field and combines target tables.
        Creates new column with the fieldname. While repititive, this will
        make Plateruns much easier to implement.

        clean_or_input: str
            contains 'clean' for targets_clean.
        """
        if 'clean' in clean_or_input:
            field_file = paths.fiveplates_clean_field_file(self.name)
        else:
            field_file = paths.fiveplates_field_file(self.name)

        data = io.load_fiveplates_field(self.platerun_name, field_file)
        data.rename_column('Catalog_id', 'catalogid')  # keep consistent with plates
        N_targets = len(data)
        field_column = Column(data=[self.name] * N_targets,
                              name='field',
                              dtype='S200')
        data.add_column(field_column)
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
        self.platesummary = io.load_fiveplates_summary(run_name)
        self.fieldnames = self._get_fields()

    def _get_fields(self):
        return list(self.platesummary['FieldName'])

    def load_fields(self):
        return [Field(fname, self.name) for fname in
                self.fieldnames]

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
            self._targets = self._load_table()
            return self._targets

    def _load_table(self):
        """
        Takes all fields within platerun and combines target tables.
        """

        table = vstack([field.targets for field in self.fields])
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





