from . import util
from . import field
from .data import plansummary
import numpy as np
from copy import copy

_summary = plansummary.load()
_summary.add_index('platerun')  # for quick filtering on fieldname
_names_array = _summary['platerun'].astype('U')  # for quick checking

def indx_in_plateruns(run_name):
    return np.where(_names_array == run_name)[0]

class PlateRun:
    """
    Class to act as interface to platerun.
    """

    def __init__(self, run_name):
        self.name = run_name
        self.fieldnames = self._get_fields()

    def _get_fields(self):
        idx = indx_in_plateruns(self.name)
        names = _summary['name'].astype('U')[idx]
        return np.unique(names)  # no field repeats

    @property
    def summary(self):
        return _summary[indx_in_plateruns(self.name)]


    def load_fields(self):
        return [field.Field(fieldname) for fieldname in
                self.fieldnames]

    @property
    def fields(self):
        try:
            return self._fields
        except AttributeError:
            self._fields = self.load_fields()
            return self._fields

    def assigned_table(self):
        """
        Table for all assigned targets in plate run.
        Has columns for plateID AND field
        """
        _plugHoles_data = copy([field._plugHoles for field in
                                self.fields])
        # Give each table a column with plate number
        _tables_w_platenums = []

        for tablist, field in zip(_plugHoles_data, self.fields):
            this_table_list = []
            for ii, tab in enumerate(tablist):
                tab['plate'] = [field._plates[ii]]  * len(tab)
                this_table_list.append(tab)
            _tables_w_platenums.append(this_table_list)

        return util.unique_cat_w_provenance(_tables_w_platenums,
                                            self.fieldnames,
                                            'field')

