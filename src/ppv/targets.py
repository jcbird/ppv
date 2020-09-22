from . import util
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

    def __init__(self, ra, dec, catalogid=None, ancillary=None, epoch=2015.5):
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
        self.epoch = epoch
        self.coords = self._construct_skycoords(ra, dec)
        self.catalogid = catalogid
        self.data = ancillary
        self._available_indx = {}
        self._assigned_indx = {}
        self._input_indx = {}
        self._clean_indx = {}

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

    def available(self, FieldorPlate):
        """
        Given a Field or Plate instance, return a boolean array of if the
        targets are available.
        """

        indx = self._available_indx.get(FieldorPlate.name,
                                        self._radial_search(FieldorPlate.center,
                                                            FieldorPlate._radius)
                                        )
        if FieldorPlate.name not in self._available_indx:
            self._available_indx[FieldorPlate.name] = indx
        return indx


    def _available(self, field):
        """

        """
        # Here, only care about index of Targets
        idx_targ = np.where(self.coords.separation(field.center) <
                            field._radius)[0]
        self._available_indx[field.name] = idx_targ
        return idx_targ

    def available_in_field(self, field, **report_kwds):
        """available.

        Parameters
        ----------
        field : class instance
            field object
        """
        indx = self._available_indx.get(field.name, self._available(field))
        return self._report(**report_kwds)[indx]

    def available(self, instance, **report_kwds):
        """available targets in field OR platerun

        Parameters
        ----------
        instance : field or platerun instance
            class instance
        """
        if util.is_platerun(instance):
            return [self.available_in_field(field, **report_kwds) for field in
                    instance.fields]
            # do platerun stuff
        else: # is field
            return self.available_in_field(instance, **report_kwds)

    def _assigned(self, field):
        """
        positional search has to happen for now because no way to directly tie targetDB in with plugHoles output (2020/09/18).
        """
        # Here, only care about index of Targets

        avail_coords = self.available_in_field(field, coords=True)
        inds = np.arange(len(avail_coords), dtype=int)
        idx_assigned = []
        for plug_coords in field.plugged_coords:
            idx_field, sep2d, _ = avail_coords.match_to_catalog_sky(plug_coords)
            max_sep = 1.0 * u.arcsec  # within one arcsec
            constraint = sep2d < max_sep
            idx_assigned.append(inds[constraint])
        self._assigned_indx[field.name] = idx_assigned
        return idx_assigned

    def assigned_in_field(self, field, **report_kwds):
        """available.

        Parameters
        ----------
        field : class instance
            field object
        """
        indx = self._assigned_indx.get(field.name, self._assigned(field))
        return [self.available_in_field(field, **report_kwds)[ind] for ind in indx]

    def assigned(self, instance, **report_kwds):
        """available targets in field OR platerun

        Parameters
        ----------
        instance : field or platerun instance
            class instance
        """
        if util.is_platerun(instance):
            return [self.assigned_in_field(field, **report_kwds) for field in
                    instance.fields]
            # do platerun stuff
        else: # is field
            return self.assigned_in_field(instance, **report_kwds)

