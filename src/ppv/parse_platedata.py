from . import _fp_available
from .data import io
from astropy.table import Table, vstack


plateruns = list(_fp_available)

platedata_tables = [io.load_fp_platedata(prun) for prun
                    in plateruns]

main_platedata = vstack(platedata_tables)
main_platedata.add_index('designid')
main_platedata.add_index('fieldname')








