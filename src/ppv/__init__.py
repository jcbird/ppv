from .data import io as data_io
from .util import download




allplate_summary = data_io.load_plansummary()
allplate_summary.add_index('name')  # for quick filtering on fieldname
_names_array = allplate_summary['name'].astype('U')  # for quick checking
_platerun_array = allplate_summary['platerun'].astype('U')  # for quick checking

available_plateruns = list(set(_platerun_array))


def update():
    """
    Updates the plate summary file via rsync. Important for adding
    new plate runs.
    """
    download.plate_plans()

    # I dislike this, feels like a dangerous hack but doing it for now.
    global allplate_summary, _names_array, _platerun_array, available_plateruns
    allplate_summary = data_io.load_plansummary()
    allplate_summary.add_index('name')  # for quick filtering on fieldname
    _names_array = allplate_summary['name'].astype('U')  # for quick checking
    _platerun_array = allplate_summary['platerun'].astype('U')  # for quick checking

    available_plateruns = list(set(_platerun_array))
    print('Plate plans summary file updated to current version.')

    # Need to update plugholes files too

    return None



