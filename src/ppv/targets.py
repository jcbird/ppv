from . import groups
from . import fiveplates
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy import units as u


class Targets:
    """
    Class to act as interface to target list of interest.

    methods
    =======

    available: relative to its own Target class

    assigned: relative to the Field
    """

    def __init__(self, ra, dec, catalogid, data=None, epoch=2015.5):
        """Constructor.
        ancillary is best used as the full table where 'ra' and 'dec' came from. Needs to be a one to one match with 'ra', 'dec'.

        Parameters
        ----------
        ra : array-like
            Right Ascension
        dec : array-like
            Declination
        catalogid : array-like
            catalogid (usually from targetDB output)
        ancillary : table or record array
            usually the targetDB table corresponding to the carton of interst
        epoch :
            epoch
        """
        # TODO find a better way to construct 'data' when ancillary is None
        self.epoch = epoch
        self.coords = self._construct_skycoords(ra, dec)
        self.catalogid = catalogid
        self.data = data
        self._available_indx = {}
        self._assigned_indx = {}
        self._input_indx = {}
        self._clean_indx = {}

    def __repr__(self):
        return f'Targets: {self.catalogid!r}'

    def __repr__(self):
        return f'{len(self.catalogid)} targets with IDs: {self.catalogid!r}'

    def _construct_skycoords(self, ra, dec):
        print('Assuming RA, Dec are in degrees and {} epoch'.format(self.epoch))
        return SkyCoord(ra=ra * u.degree, dec=dec * u.degree,
                        obstime=Time(self.epoch, format='decimalyear'))

    def _report(self, coords=None):
        if (coords==None) & (self.data is not None):
            return self.data
        else:
            return self.coords

    def _radial_search(self, center, radius):
        """
        Finds all members of Targets that are within radial cone search of
        center.

        Parameters
        ----------
        center : SkyCoord
            center coordinates
        radius : astropy quantity
            Radius of cone search. Typically 1.49 degrees for APO
        """
        return self.coords.separation(center) < radius

    def _available_in_field(self, FieldorPlate):
        """
        Given a Field or Plate instance, return a boolean array of target members
        that could be observed. Availability based on position only.
        """
        if isinstance(FieldorPlate, groups.Platerun):
            print(f'{FieldorPlate} appears to be a platerun. Use available_in_platerun method instead.')
            return
        indx = self._available_indx.get(FieldorPlate.name,
                                        self._radial_search(FieldorPlate.center,
                                                            FieldorPlate._radius)
                                        )
        if FieldorPlate.name not in self._available_indx:
            self._available_indx[FieldorPlate.name] = indx
        return indx

    def _available_in_platerun(self, platerun_):
        """
        Given a platerun, return a boolean array of all members that could be observed
        in any field of the platerun.
        """
        indx_all = [self.available_in(field) for field in platerun_.fields]
        return np.bitwise_or.reduce(indx_all)

    def available_in(self, pl_field_plrun):
        """
        Given a Plate, Field, or PlateRun instance, return a boolean array
        of target members that could be observed. Availability based on position only.
        """
        if (isinstance(pl_field_plrun, groups.Platerun) |
            isinstance(pl_field_plrun, fiveplates.Platerun)):
            return self._available_in_platerun(pl_field_plrun)
        return self._available_in_field(pl_field_plrun)  #  SAME logice for plate/field

    def _within(self, catalogIDs):
        """
        membership test of targets within array-like catalogIDs
        """
        return np.in1d(self.catalogid, catalogIDs)

    def assigned_in(self, pl_field_plrun):
        """
        Given a Plate, Field, or PlateRun instance, return a boolean array
        representing if each Target member was assigned a fiber according
        to catalogID.
        """
        indx = self._assigned_indx.get(pl_field_plrun.name,
                                       self._within(pl_field_plrun.targets['catalogid']))
        if pl_field_plrun.name not in self._assigned_indx:
            self._assigned_indx[pl_field_plrun.name] = indx
        return indx

    def assigned_info(self, pl_field_plrun):
        """
        Given a Plate, Field, or PlateRun instance, get the rows of their 
        targets table that correspond to the assigned member targets.
        """
        catalogids_ = self.catalogid[self.assigned_in(pl_field_plrun)]
        return pl_field_plrun.get_targets(catalogids_)

    def not_assigned_in(self, pl_field_plrun):
        """
        Given a Plate, Field, or PlateRun instance, return a boolean array
        representing target members that were available and were NOT assigned a fiber.
        """
        assigned_ = self.assigned_in(pl_field_plrun)
        try:
            available_ = self.available_in_platerun(pl_field_plrun)
        except (AttributeError, KeyError) as error:
            available_ = self.available_in(pl_field_plrun)
        return available_ & ~assigned_
