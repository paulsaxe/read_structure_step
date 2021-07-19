"""
The public interface to the read_structure_step SEAMM plugin
"""

from . import formats
import os


def write(
    file_name,
    configuration,
    extension=None,
    remove_hydrogens="no",
    system_db=None,
    system=None,
    printer=None,
    references=None,
    bibliography=None,
):
    """
    Calls the appropriate functions to parse the requested file.

    Parameters
    ----------
    file_name : str
        Name of the file

    configuration : Configuration
        The SEAMM configuration to write into

    extension : str, optional, default: None
        The extension, including initial dot, defining the format.

    remove_hydrogens : str = "no"
        Whether to remove hydrogen atoms before writing the structure to file.

    system_db : System_DB = None
        The system database, used if multiple structures in the file.

    system : System = None
        The system to use if adding subsequent structures as configurations.

    printer : Logger or Printer
        A function that prints to the appropriate place, used for progress.

    references : ReferenceHandler = None
        The reference handler object or None

    bibliography : dict
        The bibliography as a dictionary.

    Returns
    -------
    [Configuration]
        The list of configurations created.
    """

    if type(file_name) is not str:
        raise TypeError(
            """write_structure_step: The file name must be a string, but a
            %s was given. """
            % str(type(file_name))
        )

    if file_name == "":
        raise NameError(
            """write_structure_step: The file name for the structure file
            was not specified."""
        )

    file_name = os.path.abspath(file_name)

    if extension is None:
        raise NameError("Extension could not be identified")

    if extension not in formats.registries.REGISTERED_WRITERS.keys():
        raise KeyError(
            "write_structure_step: the file format %s was not recognized." % extension
        )

    writer = formats.registries.REGISTERED_WRITERS[extension]["function"]

    writer(
        file_name,
        configuration,
        extension=extension,
        remove_hydrogens=remove_hydrogens,
        system_db=system_db,
        system=system,
        printer=printer,
        references=references,
        bibliography=bibliography,
    )
