"""Implementation of the chemical file reader/write using Open Babel
"""

from pathlib import Path

from openbabel import openbabel

from read_structure_step.formats.registries import register_reader  # noqa: F401

# Get the list of file formats from Open Babel
obConversion = openbabel.OBConversion()
known_input_formats = obConversion.GetSupportedInputFormat()
known_output_formats = obConversion.GetSupportedOutputFormat()
del obConversion


def load_file(
    path,
    configuration,
    extension=".sdf",
    add_hydrogens=True,
    system_db=None,
    system=None,
    indices="1:end",
    subsequent_as_configurations=False,
    system_name="Canonical SMILES",
    configuration_name="sequential",
    **kwargs,
):
    """Use Open Babel for reading any of the formats it supports.

    See https://en.wikipedia.org/wiki/Chemical_table_file for a description of the
    format. This function is using Open Babel to handle the file, so trusts that Open
    Babel knows what it is doing.

    Parameters
    ----------
    file_name : str or Path
        The path to the file, as either a string or Path.

    configuration : molsystem.Configuration
        The configuration to put the imported structure into.

    extension : str, optional, default: None
        The extension, including initial dot, defining the format.

    add_hydrogens : bool = True
        Whether to add any missing hydrogen atoms.

    system_db : System_DB = None
        The system database, used if multiple structures in the file.

    system : System = None
        The system to use if adding subsequent structures as configurations.

    indices : str = "1:end"
        The generalized indices (slices, SMARTS, etc.) to select structures
        from a file containing multiple structures.

    subsequent_as_configurations : bool = False
        Normally and subsequent structures are loaded into new systems; however,
        if this option is True, they will be added as configurations.

    system_name : str = "from file"
        The name for systems. Can be directives like "SMILES" or
        "Canonical SMILES". If None, no name is given.

    configuration_name : str = "sequential"
        The name for configurations. Can be directives like "SMILES" or
        "Canonical SMILES". If None, no name is given.

    Returns
    -------
    [Configuration]
        The list of configurations created.
    """
    if isinstance(path, str):
        path = Path(path)

    path.expanduser().resolve()

    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats(extension.lstrip("."), "smi")

    obMol = openbabel.OBMol()
    obConversion.ReadFile(obMol, str(path))

    if add_hydrogens:
        obMol.AddHydrogens()

    configuration.from_OBMol(obMol)

    # Set the system name
    if system_name is not None and system_name != "":
        lower_name = system_name.lower()
        if "from file" in lower_name:
            system.name = obMol.GetTitle()
        elif "canonical smiles" in lower_name:
            system.name = configuration.canonical_smiles
        elif "smiles" in lower_name:
            system.name = configuration.smiles
        else:
            system.name = system_name

    # And the configuration name
    if configuration_name is not None and configuration_name != "":
        lower_name = configuration_name.lower()
        if "from file" in lower_name:
            configuration.name = obMol.GetTitle()
        elif "canonical smiles" in lower_name:
            configuration.name = configuration.canonical_smiles
        elif "smiles" in lower_name:
            configuration.name = configuration.smiles
        elif lower_name == "sequential":
            configuration.name = "1"
        else:
            configuration.name = configuration_name

    return [configuration]
