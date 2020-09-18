from astropy.table import Table
from pathlib import Path

data_dir = Path.cwd().parent / 'data/raw'

selected_file = data_dir / 'mwm_planet_0.1.0.fits.gz'
sel_targDB_file = data_dir / 'mwm_planet_0.1.0_targetdb.fits.gz'


sel_targ = Table.read(selected_file.as_posix())
sel_targDB = Table.read(sel_targDB_file.as_posix())

sel_targ.sort('catalogid')
sel_targDB.sort('catalogid')

# Now they are matching rows

# sel_targDB is input for Target class
