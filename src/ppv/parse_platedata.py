from . import _fp_available
from .data import io
from .util import paths
from astropy.table import Table, vstack


plateruns = list(_fp_available)
platedata_paths = [paths.fp_platedata(prun) for prun in plateruns]

prun_to_path = dict(zip(plateruns, platedata_paths))

pruns_to_parse_path = dict(filter(lambda prun_path: prun_path[1], prun_to_path.items()))
pruns_to_parse = list(pruns_to_parse_path.keys())

platedata_tables = [io.load_fp_platedata(prun) for prun
                    in pruns_to_parse]

platedata_tables = list(filter(None, platedata_tables))

main_platedata = vstack(platedata_tables)
main_platedata.add_index('fieldname')
main_platedata.add_index('designid')








