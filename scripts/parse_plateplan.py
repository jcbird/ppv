from astropy.table import Table
from astropy.io.registry import (register_identifier, register_reader,
                                 register_writer)
from pydl.pydlutils.yanny import (is_yanny, read_table_yanny,
                                  write_table_yanny, yanny)
from pathlib import Path
import numpy as np
import ppv.config

register_identifier('yanny', Table, is_yanny)
register_reader('yanny', Table, read_table_yanny)
register_writer('yanny', Table, write_table_yanny)

platePlans = Table.read('../data/raw/platePlans.par', format='yanny',
                tablename='PLATEPLANS')

print('platePlans.par is read')

is_mwm_plate = np.array(['mwm' in prun for prun in platePlans['platerun']])
is_bhm_plate = np.array(['bhm' in prun for prun in platePlans['platerun']])
is_sdss5_plate = np.bitwise_or(is_mwm_plate, is_bhm_plate)


sdss5_plates = platePlans[is_sdss5_plate]
# parent in root directory of repository

dir_ = (Path.cwd().parent / ppv.config._src_dir) / 'data'
out_filename = (dir_ / 'platePlans_sdss5.fits').as_posix()

sdss5_plates.write(out_filename, overwrite='True', format='fits')
print(f'SDSS-V platePlans table written to {out_filename}')

