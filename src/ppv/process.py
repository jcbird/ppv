"""
Contains functions that move a field from one stage of the plate design
process to the next. 
Initially, function to replicate processing the fiveplates outputs through
plate design to get a better idea of what WILL be observed.

"""

from astropy.table import Column, vstack
import numpy as np
from numpy.random import Generator, PCG64

"""
per field:

    get NSCI apogee, NSCI boss,
    get NSTD, NSKY
    all of the above from defaultparameters

    convert targets table to DF
    group by order_priority

    start at highest priorirty:
       randomly select (maybe astropy bootstrap this)


    Takes in an astropy table containing a list of targets and . This is almost
"""


def simulate_platedesign(fp_targets, nSCI_apogee, nSCI_boss,
                         random_seed=1050):
    """
    Takes in an astropy table containing a list of fiveplates targets and 
    simulates the plate design code to produce an estimate of what the final
    plate will look like. To do this, we go through priority group by priority
    group.

    Parameters
    ----------
    fp_targets : astropy table
        Almost always the output of fiveplates.Field.targets
    nSCI_apogee : int
        Number of APOGEE fibers for science in plate.
    nSCI_boss : int
        Number of BOSS fibers for science in plate.
    random_seed : int
        Seed number for random number generator. Set to any number.
        Default is 1050 (just *randomly* chosen) for reproducability.
    """

    # Initiate Random State (fixed)
    RandomState = Generator(PCG64(1050))
    # numpy random functions will use this

    # indx_col = Column(np.arange(len(fp_targets), dtype=int), name='indx')
    # priority_groups = fp_targets['order_priority'].data
    # indx_groups = indx_col.group_by(priority_groups)

    bypriority = fp_targets.group_by('order_priority')
    assigned_targets = []

    nSCI_apogee_assigned = 0   # nothing assigned at beginning
    nSCI_boss_assigned = 0

    nSCI_goal = {}
    nSCI_assigned = {}
    nSCI_needed = {}

    nSCI_goal['apogee'] = nSCI_apogee
    nSCI_goal['boss'] = nSCI_boss
    nSCI_assigned['apogee'] = nSCI_apogee_assigned
    nSCI_assigned['boss'] = nSCI_boss_assigned

    for ii, target_grp in enumerate(bypriority.groups):
        nSCI_needed['apogee'] = nSCI_goal['apogee'] - nSCI_assigned['apogee']
        nSCI_needed['boss'] = nSCI_goal['boss'] - nSCI_assigned['boss']

        # consider = bypriority.groups[priority]
        instrument_ = set(target_grp['instrument']).pop()
        # beter be only ONE instrument!!!
        Nrows = len(target_grp)
        # Ignore SKY and STD cartons for now
        target_type = set(target_grp['Type']).pop()

        if target_type != 0:
            continue    # SKIP this group

        if Nrows <= nSCI_needed[instrument_]:
            # Just take whole priority group if it will fit
            assigned_targets.append(target_grp)
            nSCI_assigned[instrument_] += Nrows  # increase N of fibers assigned
        elif nSCI_needed[instrument_] > 0 :   #  Still need to assign fibers
            keep_rows_indx = RandomState.choice(Nrows,
                                              nSCI_needed[instrument_],
                                              replace=False)
            assigned_targets.append(target_grp[keep_rows_indx])
            nSCI_assigned[instrument_] += len(keep_rows_indx)
        else:  # Filled up the plate already
            pass

    assigned = vstack(assigned_targets)
    assigned.sort('catalogid')
    return assigned
