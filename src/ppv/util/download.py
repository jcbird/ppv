from .. import config

import os
import subprocess
import shlex

_base_server = 'apogee.sdss.org'
_base_url = '///uufs/chpc.utah.edu/common/home/sdss05/software/svn.sdss.org/data/sdss/platelist/trunk'
_plates = 'plates'


def plugHoles_batch(plate_batch, dry_run=False, execute=True):
    """
    Will download the appropriate directories (matching dir structure at Utah)
    and plugHoles-*.par files.
    This command will use subprocess to call rsync based on the parameters in
    the ppv_setup.ini file.
    To simply print the command to the screen (and NOT run it), use execute=False.
    To print all files that would be copied without any actual writes to disk, use
    dry_run=True.
    Otherwise, the user should never have to call this command.

    Parameters
    ----------
    plate_batch : str
        e.g., '0150XX'. However, plate_batch is usually automatically
        generated using util.paths.plate_batch
    dry_run : boolean
        dry_run
    execute : boolean
        execute

    """
    if config.plate_dir.exists():
        pass
    else:
        os.makedirs(config.plate_dir)

    dry_opt = ''

    if dry_run:
        dry_opt = '--dry-run '

    preamble = f"rsync {dry_opt}-avz --include='plateHoles-*.par' --include='*/' --exclude='*'"
    source = f"{_base_server}:{_base_url}/plates/{plate_batch}/"
    destination = f"{os.fspath(config.plate_dir)}/{plate_batch}/"
    rsync_cmd = f"{preamble} {config.utah_username}@{source} {destination}"

    if execute is False:
        return rsync_cmd

    rsync_cmd = shlex.split(rsync_cmd)
    subprocess.check_call(rsync_cmd)
    return None


# TODO make function for plateplans.par file
