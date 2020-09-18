from .util import paths
from astropy.table import Table
from pydl.pydlutils.yanny import yanny
import numpy as np


fields = ['target_ra', 'target_dec', 'holetype', 'targettype', 'catalogid', 
          'tmass_id', 'firstcarton', 'tmass_h', 'gaia_g', 'gaia_rp',
          'gaia_bp']
dtypes = [np.float, np.float, 'U', 'U', np.uint,
          'U23', 'U', np.float, np.float, np.float,
          np.float]

_field_dtypes = [(name, dtype) for name, dtype in zip(fields, dtypes)]


def load_yanny(platenum):
    filepath = paths.plateholes(platenum).as_posix()
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
