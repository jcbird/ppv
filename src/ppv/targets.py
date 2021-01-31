from . import groups
from . import fiveplates
import numpy as np
from astropy.table import Table
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

    def __init__(self, data, colnames=['catalogid', 'ra', 'dec'],
                 epoch=2015.5):
        """
        Creates a targets object.

        The targets object requires at least catalogIDs to work.
        To check on target availability, RA and Dec must also be provided.
        Any other column (if data is a table) or field (if data is a record array)
        or key:value pair (if data is a dict) will be kept as ancillary data
        for convenience.

        Using an astropy table is by far the most robust method to construct
        a targets object.

        Parameters
        ----------
        data : astropy table, numpy record array, or dict
            N x C in shape, where N is the number of targets and C is the number
            of different columns.
        colnames : list of strings
            List of column/field names corresponding to the catalogID (required)
            and RA, Dec (optional, but recommended) of the targets.
            *Order is fixed and MUST follow [catalogID, RA, Dec] format.*
        epoch : int
            Epoch of target positions.
        """
        self.epoch = epoch
        self._colnames = {'catalogid': colnames[0],
                          'ra': colnames[1],
                          'dec': colnames[2]}
        self.data = self._make_table(data)
        ### self.ra = self.
        self.catalogid = self._get('catalogid')
        self.coords = self._construct_skycoords(self._get('ra'),
                                                self._get('dec'))
        self._available_indx = {}
        self._assigned_indx = {}
        self._input_indx = {}
        self._clean_indx = {}
        # All indx dictionaries will now have keys of tuple (field.name, platerun.name)

    def __repr__(self):
        return f'Targets: {self.catalogid!r}'

    def __repr__(self):
        return f'{len(self.catalogid)} targets with IDs: {self.catalogid!r}'

    def _make_table(self, data):
        """
        Converts to astropy table AND sorts all by catalogID.
        The sorting is useful for get_info method (and matching plate files).
        """
        tab = Table(data)
        tab.sort(self._colnames['catalogid'])
        return tab

    def _get(self, name):
        """
        Maybe column names
        """
        return self.data[self._colnames[name]]

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
        lookup_key =-(FieldorPlate.name, FieldorPlate.platerun)
        indx = self._available_indx.get(lookup_key,
                                        self._radial_search(FieldorPlate.center,
                                                            FieldorPlate._radius)
                                        )
        if FieldorPlate.name not in self._available_indx:
            self._available_indx[lookup_key] = indx
        return indx

    def _available_in_platerun(self, platerun_):
        """
        Given a platerun, return a boolean array of all members that could be observed
        in any field of the platerun.
        """
        print(f"""Please be patient.
                  Initial target loading for Platerun can take up to 1 second per field.
                  Loading target data from {len(platerun_.fieldnames)} Fields...""", flush=True)
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

    def assigned_in(self, pl_field_plrun, table='targets'):
        """
        Given a Plate, Field, or PlateRun instance, return a boolean array
        representing if each Target member was assigned a fiber according
        to catalogID.
        """
        if (isinstance(pl_field_plrun, groups.Platerun) |
            isinstance(pl_field_plrun, fiveplates.Platerun)):
            lookup_key = (pl_field_plrun.name, table)
        else:
            lookup_key = (pl_field_plrun.name, pl_field_plrun.platerun, table)
        _lookin_table = getattr(pl_field_plrun, table)
        indx = self._assigned_indx.get(lookup_key,
                                       self._within(_lookin_table['catalogid']))
        if lookup_key not in self._assigned_indx:
            self._assigned_indx[lookup_key] = indx
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
        available_ = self.available_in_platerun(pl_field_plrun)
        return available_ & ~assigned_
