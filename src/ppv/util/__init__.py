import pprint
from astropy.table import Column

pp = pprint.PrettyPrinter(indent=4)


def scalar_column(value, Nrows, name):
    """
    Create a column for an astropy table with a repeating value.

    Parameters
    ----------
    value : int, string, float, object scalar value
        Value to fill the column with.
    Nrows : int
        Length of column
    name : string
        Name of column
    """
    return Column(data= [value] * Nrows,
                  name= name,
                  dtype= type(value))

