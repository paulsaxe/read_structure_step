from . import obabel
from read_structure_step.formats.registries import register_format_checker

keywords = ['@<TRIPOS>']

@register_format_checker('.mol2')
def check_format(data):

    if all(keyword in data for keyword in keywords):
        return True
    else:
        return False
