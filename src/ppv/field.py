from .data import io as data_io
from . import plate
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time

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
        self._plates = plates_of_field(self.name)
        self._summary_indx = indx_in_plateruns(self.name)
        self.raCen, self.decCen = self._center()
        self.center = SkyCoord(self.raCen, self.decCen,
                               obstime=Time(2015.5, format='decimalyear'))
        self.platerun, self.programname = self.meta()
        self._radius = 1.49 * u.degree
        self._plugHoles = [plate.get_table(platenum) for platenum in self._plates]

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
        Coordinates of targets assigned fibers on plate
        """
        try:
            return self._plugcoords
        except AttributeError:
            return self._construct_skycoords()



    def _center(self):
        ra = allplate_summary['raCen'][self._summary_indx][0]
        dec = allplate_summary['decCen'][self._summary_indx][0]
        return ra * u.deg, dec * u.deg


    def meta(self):
        prun = allplate_summary['platerun'][self._summary_indx][0]
        programname = allplate_summary['programname'][self._summary_indx][0]
        return prun, programname






