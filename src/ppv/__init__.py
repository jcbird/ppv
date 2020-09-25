from .data import io as data_io

allplate_summary = data_io.load_plansummary()
allplate_summary.add_index('name')  # for quick filtering on fieldname
_names_array = allplate_summary['name'].astype('U')  # for quick checking
_platerun_array = allplate_summary['platerun'].astype('U')  # for quick checking

available_plateruns = list(set(_platerun_array))
