from .data import io as data_io
from . import plate
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import vstack, Column

allplate_summary = data_io.load_plansummary()
allplate_summary.add_index('name')  # for quick filtering on fieldname
_names_array = allplate_summary['name'].astype('U')  # for quick checking

def field_in_plateruns(fieldname):
    return allplate_summary.loc[fieldname]

def indx_in_plateruns(fieldname):
    return np.where(_names_array == fieldname)[0]

def plates_of_field(fieldname):  # returns a list
    plates = allplate_summary['plateid'][indx_in_plateruns(fieldname)]
    return plates.tolist()





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
        self.center = SkyCoord(self.ra, self.dec,
                               obstime=Time(2015.5, format='decimalyear'))
        # TODO check epoch of field designation
        self.platerun, self.programname = self.meta()
        self._radius = 1.49 * u.degree
        self._plates = [plate.Plate(platenum) for platenum in self._platenums]
        # self._plugHoles = [plate.get_table(platenum) for platenum in self._plates]

    def __repr__(self):
        return f'Field({self.fieldname!r})'

    def __str__(self):
        first = f'Field: {self.fieldname!r}, RA: {self.ra!r}, Dec: {self.dec!r}'
        second = f'Plate Numbers: {self._platenums!r}'
        return first + second

    @property
    def plates(self):
        return self._plates

    def _center(self):
        ra = allplate_summary['raCen'][self._summary_indx][0]
        dec = allplate_summary['decCen'][self._summary_indx][0]
        return ra * u.deg, dec * u.deg

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

        table = vstack([pl.targets for pl in self._plates])
        N_targets = len(table)
        field_column = Column(data=[self.name] * N_targets,
                              name='field',
                              dtype='str')
        table.add_column(field_column)
        return table

    def meta(self):
        prun = allplate_summary['platerun'][self._summary_indx][0]
        programname = allplate_summary['programname'][self._summary_indx][0]
        return prun, programname

    # TODO turn this around for getting info from table
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
    def __init__(self):
        pass

    @property
    def fields(self):
        # load_fields
        pass

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

        table = vstack([field.targets for field in self._plates])
        N_targets = len(table)
        field_column = Column(data=[self.name] * N_targets,
                              name='field',
                              dtype='str')
        table.add_column(field_column)
        return table



