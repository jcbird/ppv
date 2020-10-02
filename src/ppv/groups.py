from . import allplate_summary, _names_array, _platerun_array
from . import plate, available_plateruns
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import vstack, Column


def indx_in_plateruns(fieldname):
    return np.where(_names_array == fieldname)[0]

def plates_of_field(fieldname):  # returns a list
    plates = allplate_summary['plateid'][indx_in_plateruns(fieldname)]
    return plates.tolist()

def in_platerun(run_name):
    return np.where(_platerun_array == run_name)[0]


class Field:
    """
    Class to act as interface to fields.
    """

    def __init__(self, fieldname):
        """
        fieldname is string. Look for fieldnames in allplate_summary OR
        in plate_run.fieldnames
        """
        self.name = fieldname
        self._platenums = plates_of_field(self.name)
        self._summary_indx = indx_in_plateruns(self.name)
        self.ra, self.dec = self._center()
        self.center = SkyCoord(self.ra * u.deg, self.dec * u.deg,
                               obstime=Time(2015.5, format='decimalyear'))
        # TODO check epoch of field designation
        self.platerun, self.programname = self.meta()
        self._radius = 1.49 * u.degree
        self._plates = [plate.Plate(platenum) for platenum in self._platenums]
        # self._plugHoles = [plate.get_table(platenum) for platenum in self._plates]

    def __repr__(self):
        return f'Field({self.name!r})'

    def __str__(self):
        first = f'Field: {self.name!r}, RA: {self.ra!r}, Dec: {self.dec!r}\n'
        second = f'Plate Numbers: {self._platenums!r}'
        return first + second

    @property
    def plates(self):
        return self._plates

    def _center(self):
        ra = allplate_summary['raCen'][self._summary_indx][0]
        dec = allplate_summary['decCen'][self._summary_indx][0]
        return ra, dec

    def _construct_skycoords(self):
        self._plugcoords = [SkyCoord(phole['target_ra'] * u.degree,
                            phole['target_dec'] * u.degree,
                            obstime=Time(2015.5, format='decimalyear')) for 
                            phole in self._plugHoles]
        return self._plugcoords


    @property
    def plate_data(self):
        """
        Table(s) of data from yanny files describing plate(s).
        """
        return self._plugHoles

    @property
    def plugged_coords(self):
        """
        self.targets = self._load_table()
        Coordinates of targets assigned fibers on plate
        """
        try:
            return self._plugcoords
        except AttributeError:
            return self._construct_skycoords()

    @property
    def targets(self):
        try:
            return self._targets
        except AttributeError:
            self._targets = self._load_table()
            return self._targets

    def _load_table(self):
        """
        Takes all converts plates in field and combines target tables.
        Creates new column with the fieldname. While repititive, this will
        make Plateruns much easier to implement.
        """

        table = vstack([pl.targets for pl in self.plates])
        N_targets = len(table)
        field_column = Column(data=[self.name] * N_targets,
                              name='field',
                              dtype='S200')
        table.add_column(field_column)
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
        Return rows of the Field targets table given a list of catalogIDs
        """
        return self.targets[self._contains(catalogIDs)]

    def meta(self):
        prun = allplate_summary['platerun'][self._summary_indx][0]
        programname = allplate_summary['programname'][self._summary_indx][0]
        return prun, programname

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
    Class to act as interface to platerun.
    """

    def __init__(self, run_name):
        if _check_platerun(run_name):
            pass  # all is well, platerun available
        self.name = run_name
        self.fieldnames = self._get_fields()

    def _get_fields(self):
        idx = in_platerun(self.name)
        names = allplate_summary['name'].astype('U')[idx]
        return np.unique(names)  # no field repeats

    @property
    def platesummary(self):
        return allplate_summary[in_platerun(self.name)]


    def load_fields(self):
        return [Field(fname) for fname in
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
            third = ' Run ppv.update() to update your platerun summary file and try again.'
            fourth = f'\n ======================================================== \n'
            return first + second + third + fourth
            # return f'PlateRunMissingError, {self.message} is not an available platerun'
        else:
            return 'PlateRunMissingError has been raised'


def _check_platerun(run_name):
    if run_name in available_plateruns:
        return True     # All is well
    else:  # platerun NOT available
        raise PlateRunMissingError(run_name)





