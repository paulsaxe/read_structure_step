import os
import pkgutil
import sys
import importlib

path = os.path.join(os.path.dirname(__file__))
modules = pkgutil.iter_modules(path=[path])

for loader, mod_name, ispkg in modules:
    # Ensure that module isn't already loaded
    if mod_name not in sys.modules and ispkg is True:
        # Import module

        importlib.import_module("read_structure_step.formats." + mod_name)

del os, pkgutil, sys, importlib
