import os
import pkgutil
import sys
import importlib

from .registries import last_resort_reader
from .openbabel_io.obabel import known_input_formats
from .openbabel_io.obabel import load_file

path = os.path.join(os.path.dirname(__file__))
modules = pkgutil.iter_modules(path=[path])

for loader, mod_name, ispkg in modules:
    # Ensure that module isn't already loaded

    if mod_name == "pdb":
        # the name 'pdb' my also refer to the python debugger pdb
        importlib.import_module("read_structure_step.formats.pdb")

    else:
        if mod_name not in sys.modules and ispkg is True:
            # Import module
            importlib.import_module("read_structure_step.formats." + mod_name)

del os, pkgutil, sys, importlib

# Finally register the Open Babel reader as the last resort
last_resort_reader(known_input_formats, load_file)
