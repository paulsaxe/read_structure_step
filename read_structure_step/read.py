from . import utils
from . import formats

def read(file_name, extension=None):
    """
    Calls the appropriate functions to parse the requested
    file.

    Parameters
    ----------
    file_names: str
        Name of the file

    Returns
    -------
    ret : dict
        A dictionary with the information of the input files. 
        The structure of the dictionary is the SEAMM structure format.
    """

    if file_name is None:
        raise NameError('read_structure_step: The file name for the structure file was not specified.')

    if extension is None:

        extension = utils.guess_extension(file_name)

        if extension not in formats.registries.REGISTERED_READERS.keys():
            raise KeyError('read_structure_step: the file format %s was not recognized.' % extension)

    reader = formats.registries.REGISTERED_READERS[extension]

    return reader(file_name)
