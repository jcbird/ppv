from .. import config
import os
import subprocess
import shlex
import getpass
import pexpect

_base_server = 'apogee.sdss.org'
_base_url = '///uufs/chpc.utah.edu/common/home/sdss05/software/svn.sdss.org/data/sdss/platelist/trunk'
_plates = 'plates'



def _rsync_task(rsync_command_string):
    """
    prints out rsync command, gets password, and executes.
    Usefuly for single rsync tasks.
    """
    if config.utah_username == 'NONE':
        print('Skipping rsync process because username is NONE')
        print('ppv will assume all files are available.')
        print('Continue.')
        return None
    else:
        # Continue on if not NONE
        print('Running command....')
        print(rsync_command_string)
        utah_passwd = _ask_password()
        rsync_pipe = _run_rsync(rsync_command_string, utah_passwd)
        del utah_passwd  # better to do this, no reference
        return rsync_pipe


def _ask_password():
    print(f'\n\nEnter password for {config.utah_username}: ')
    utah_passwd = getpass.getpass()
    return utah_passwd


def _run_rsync(rsync_command_string, utah_passwd):
    rsync_child = pexpect.spawn(rsync_command_string, timeout=4800)
    _prompt = rsync_child.expect(['[P/p]assword:', 'continue connecting (yes/no)?'], timeout=5)
    if _prompt == 0 :
        rsync_child.sendline(utah_passwd)
    elif _prompt == 1:
        rsync_child.sendline('yes')
        rsync_child.expect('[P/p]assword: ')
        rsync_child.sendline(utah_passwd)
    print('Starting rsync process....')
    rsync_child.read()
    rsync_child.close()
    del utah_passwd  # get rid of any reference to password
    if rsync_child.exitstatus == 0:
        print('rsync command ran successfully.')
    return rsync_child


def plugHoles_batch(plate_batch, dry_run=False, execute=True, output=False):
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
    output : boolean
        if output is True, return the pexpect object used to spawn rsync
    """
    _check_for_plate_dir()
    dry_opt = _get_dry_run_str(dry_run)

    preamble = f"rsync {dry_opt}-avz --include='plateHoles-*.par' --include='*/' --exclude='*'"
    source = f"{_base_server}:{_base_url}/plates/{plate_batch}/"
    destination = f"{os.fspath(config.plate_dir)}/{plate_batch}/"
    rsync_cmd = f"{preamble} {config.utah_username}@{source} {destination}"

    if execute is False:
        return rsync_cmd

    rsync_pipe = _rsync_task(rsync_cmd)
    if output:
        return rsync_pipe
    return None


def plate_plans(dry_run=False, execute=True, output=False):
    """
    Will download/update the platePlans.par file. This gives the plate summary file.
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
    output : boolean
        if output is True, return the pexpect object used to spawn rsync
    """
    _check_for_plate_dir()
    dry_opt = _get_dry_run_str(dry_run)

    preamble = f"rsync {dry_opt}-avz"
    source = f"{_base_server}:{_base_url}/platePlans.par"
    destination = f"{os.fspath(config.plate_dir)}/"
    rsync_cmd = f"{preamble} {config.utah_username}@{source} {destination}"

    if execute is False:
        return rsync_cmd

    rsync_pipe = _rsync_task(rsync_cmd)
    if output:
        return rsync_pipe
    return None


def _check_for_plate_dir():
    if config.plate_dir.exists():
        pass
    else:
        os.makedirs(config.plate_dir)
    return None

def _get_dry_run_str(dry_run):
    if dry_run:
        return '--dry-run '
    else:
        return ''


# TODO make function for plateplans.par file
