from .. import platerun
from astropy.table import vstack, unique
from copy import copy
import pprint


pp = pprint.PrettyPrinter(indent=4)


def is_platerun(obj):
    """
    returns True if object is a platerun.
    """
    return isinstance(obj, platerun.PlateRun)


def unique_cat(lst_of_tables):
    """unique_cat.
    Takes a list of astropy tables, concatenates them, and gets rid of 
    duplicate rows.

    Parameters
    ----------
    lst_of_tables :
        lst_of_tables
    """
    return unique(vstack(lst_of_tables))

def unique_cat_w_provenance(lst_of_tables, lst_of_properties, prop_colname):
    """unique_cat.
    Takes a list of astropy tables, concatenates them, and gets rid of 
    duplicate rows. Also adds the concatenation variable (field usually,
    sometimes plate) to table.

    Parameters
    ----------
    lst_of_tables :
        lst_of_tables
    """
    tables = copy(lst_of_tables)
    tables_good = []
    for tablist, prop in zip(tables, lst_of_properties):
        for tab in tablist:
            if len(tab) > 0:
                tab[prop_colname] = [prop] * len(tab)
                tables_good.append(tab)
    # TODO above assumes 1-lenth mini lists
    return unique_cat(tables_good)

