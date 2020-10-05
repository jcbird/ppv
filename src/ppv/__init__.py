from .data import io as data_io
from .util import download, paths



class Summary:
    """
    Container for important platerun summary info.
    In class so it can be updated dynamically.
    """

    def __init__(self):
        self._load()

    def __str__(self):
        first = f'Information container for ppv'
        second = f'Available properties: {*self._available_commands,}'
        return f'{first}\n{second}'

    def __repr__(self):
        first = f'Information container for ppv'
        second = f'Available properties: {*self._available_commands,}'
        return f'{first}\n{second}'

    def _available_commands(self):
        return [cmd for cmd in self.__dir__() if cmd[0] != '_']

    def _load(self):
        """
        Load summary and parse it
        """
        allplate = data_io.load_plansummary()
        allplate.add_index('name')  # for quick filtering on fieldname
        self._allplate = allplate
        self._names_array = allplate['name'].astype('U')  # for quick checking
        self._platerun_array = allplate['platerun'].astype('U')  # for quick checking
        self._available_plateruns = list(set(self._platerun_array))
        return None

    @property
    def allplate(self):
        try:
            return self._allplate
        except AttributeError:
            self.load()
            return self._allplate

    @property
    def fieldnames(self):
        """
        All fieldnames in platerun summary
        """
        try:
            return self._names_array
        except AttributeError:
            self.load()
            return self._names_array

    @property
    def available_plateruns(self):
        """
        All fieldnames in platerun summary
        """
        try:
            return self._available_plateruns
        except AttributeError:
            self.load()
            return self._available_plateruns

    @property
    def plateid(self):
        """
        All plate ID numbers in platerun summary
        """
        try:
            return self._allplate['plateid'].astype('int')  # for quick checking
        except AttributeError:
            self.load()
            return self._allplate['plateid'].astype('int')  # for quick checking

    @property
    def plate_batches(self):
        """
        Get a list of all available plate batches according to platePlans.par file.
        """
        batches = [paths.plate_batch(plateid).name for plateid in self.plateid]
        return list(set(batches))

    def reload(self):
        """
        re-initialize same object, needed in case of dynamic updates
        to platePlan file.
        """
        self._load()

    def update_platefiles(self):
        """
        Updates the plate summary file and all plugHoles files via rsync.
        Important for adding new plate runs and updating files in one go.
        """
        # Get the latest plate_plan file, construct rsync cmd
        print('Running rsync commands to get latest platePlans.par and plugHoles files at Utah.\n')
        utah_passwd = download._ask_password()
        plateplan_cmd = download.plate_plans(execute=False)
        print('Running command:')
        print(plateplan_cmd)
        download._run_rsync(plateplan_cmd, utah_passwd)

        self.reload()   # update the summary object
        # Get unique plate batches from updated platePlan summary file
        # construct rsync scripts for each plate batch
        batches_rsync_cmds = [download.plugHoles_batch(batch, execute=False) for
                              batch in self.plate_batches]
        print('Running command:')
        for rsync_cmd in batches_rsync_cmds:
            print(rsync_cmd)
            download._run_rsync(rsync_cmd, utah_passwd)

        del utah_passwd  #  better to delete any reference to passwd
        print('Update complete!\n')
        print(f'Latest versions now available for platePlans.par and plugHoles files for batches:\n')
        print(f'{*self.plate_batches,} plate batches')
        return None


ppv = Summary()
