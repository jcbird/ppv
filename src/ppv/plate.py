from .util import paths, download
from . import util, config
from astropy.table import Table, Column
from astropy.coordinates import SkyCoord
from astropy.time import Time
from pydl.pydlutils.yanny import yanny
import astropy.units as u
import os
import numpy as np


fields = ['target_ra', 'target_dec', 'holetype', 'targettype', 'catalogid', 
          'tmass_id', 'firstcarton', 'tmass_h', 'gaia_g', 'gaia_rp',
          'gaia_bp', 'epoch']
dtypes = [np.float, np.float, 'U', 'U', np.uint,
          'U23', 'U', np.float, np.float, np.float,
          np.float, np.float]

_field_dtypes = [(name, dtype) for name, dtype in zip(fields, dtypes)]


def load_yanny(platenum):
    platepath = paths.plateholes(platenum)

    if platepath.exists():
        pass
    else:  # need to get plugHoles files
        platebatch_path = paths.plate_batch(platenum)
        platebatch = platebatch_path.name
        print(f'{os.fspath(platepath)} does not exist. Getting files via rsync now')
        print(f'--- Please enter your password for {config.utah_username} below --')
        download.plugHoles_batch(platebatch)

    filepath = os.fspath(paths.plateholes(platenum))
    pholes_obj = yanny(filepath, raw=True)
    return pholes_obj

def get_dict(platenum):
    pholes_obj = load_yanny(platenum)
    holes_dict = pholes_obj['STRUCT1']
    return holes_dict

# TODO make get table more flexible (different columns)
def get_table(platenum):
    holes_dict = get_dict(platenum)
    data = [np.array(holes_dict[field], dtype=dd) for field, dd
            in _field_dtypes]
    plate_table = Table(data=data,
                        names=fields)
    return plate_table

def yanny_to_dict(yanny_obj):
    holes_dict = yanny_obj['STRUCT1']
    return holes_dict

def dict_to_table(yanny_dict):
    data = [np.array(yanny_dict[field], dtype=dd) for field, dd
            in _field_dtypes]
    plate_table = Table(data=data,
                        names=fields)
    return plate_table



class Plate():
    """
    Container class for plate and plugHoles data.
    Typically used to read in plugHoles parameter files.
    """

    def __init__(self, platenum):
        """

        Parameters
        ----------
        platenum : int
            Number of plate; e.g., 15004
        """
        self.platenum = platenum
        self.name = platenum
        # load plugHoles parameter file
        self._plugHoles = load_yanny(platenum)
        self.targets = self._load_table()
        self.ra, self.dec = self._center()
        self._radius = 1.49 * u.degree  # assuming APO
        self._epoch = self._get_epoch()
        self.center = SkyCoord(self.ra * u.degree, self.dec * u.degree,
                               obstime=Time(self._epoch, format='decimalyear'))


    def __repr__(self):
        return f'Plate({self.platenum!r})'

    def __str__(self):
        return f'Plate: {self.platenum!r}; RA: {self.ra}; Dec: {self.dec}'

    def _center(self):
        return float(self._plugHoles['raCen']), float(self._plugHoles['decCen'])

    def __getattr__(self, attr):
        """
        Gets column for plate data table.
        """
        return self.targets[attr]

    def property(self, keyword):
        """
        Convenience function for accessing properties of plugHoles parameter file.
        This is for values BEFORE the table.
        """
        return self._plugHoles[keyword]

    def properties(self):
        """
        Shows all available properties in the plugHoles parameter file.
        """
        return util.pp.pprint(list(self._plugHoles.keys()))

    # TODO Ensure that the platerun string always contains the correct epoch

    def _get_epoch(self):
        """
        Gets the epoch of the plate drilling from the epoch of the first science target.
        As far as I know, no other way to do this from the plate par file only.
        """
        is_science = self.targets['targettype'] == 'science'
        first_science_idx = np.argwhere(is_science)[0][0]
        return self.targets[first_science_idx]['epoch']

    def _load_table(self):
        """
        converts STRUCT1 of yanny object to astropy table.
        Creates new column with the platenumber. While repititive, this will
        make Fields and Plateruns much easier to implement.
        """
        table = dict_to_table(yanny_to_dict(self._plugHoles))
        N_targets = len(table)
        plate_column = Column(data=[self.platenum] * N_targets,
                              name='plate',
                              dtype=np.int)
        table.add_column(plate_column)
        table.sort('catalogid')   # sort by catalogID
        return table

    def columns(self):
        """
        Shows all available columns in target data table.
        """
        return self.targets.colnames


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
        """get_rows.

        Parameters
        ----------
        row_indx : array-like
            Boolean mask OR array of indicies to index the plugHoles table.
            Indexes the self.targets attribute.

        """
        return self.targets[self._contains(catalogIDs)]

    def __contains__(self, catIDs):
        """
        Checks for membership in a plate based on catalogID.
        ALL catIDs must be in plate to return True.

        Parameters
        ----------
        catIDs : array-like
            List of catalogIDs.
        """
        try: # already array-like
            return np.in1d(catIDs, self.catalogid)
        except TypeError:
            return np.all(np.in1d(np.array([catIDs]), self.catalogid))



