from .data import io
from astropy.table import Table, vstack


# TODO Hardcoding runs with usable plate_data files
# until a system is in place

good_runs= ['2020.10.x.mwm-bhm',
            '2020.10.y.mwm-bhm',
            '2020.09.y.bhm-mwm']


# Constuct master plate_data file

standard_names = ['FieldName',
                  'PlateID',
                  'DesignID',
                  'LocationID',
                  'RA',
                  'Dec',
                  'Epoch',
                  'Radius',
                  'HA',
                  'CadenceCategory',
                  'Priority',
                  'FiberFilling',
                  'NSky_APOGEE',
                  'NStd_APOGEE',
                  'NSky_BOSS',
                  'NStd_BOSS',
                  'Platerun']

platedata_tables = [io.load_fp_platedata(prun) for prun
                    in good_runs]


pd_colnames = [tab.colnames for tab in platedata_tables]
pd_colnames_lower = [[col.lower() for col in col_list] for col_list in pd_colnames]

# Fix the 'Notes' column, just put in the platerun if available
for ii, pd_table in enumerate(platedata_tables):
    try:
        notes_col_indx = pd_colnames_lower[ii].index('notes')
        prun_name = good_runs[ii]
        Nrows = len(pd_table)
        pd_table[pd_colnames[ii][notes_col_indx]] = [prun_name] * Nrows
    except ValueError:  # no Notes column
        pass


# Rename columns to be the same
for pd_table in platedata_tables:
    pd_table.rename_columns(pd_table.colnames, standard_names)

main_platedata = vstack(platedata_tables)
main_platedata.add_index('FieldName')
main_platedata.add_index('DesignID')








