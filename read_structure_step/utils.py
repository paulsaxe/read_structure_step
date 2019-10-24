import os
from . import formats
import re


def guess_extension(file_name, with_file_name=False):

    if with_file_name is True:
        (root, ext) = os.path.splitext(file_name)
        return ext.lower()


    available_extensions = formats.registries.REGISTERED_FORMAT_CHECKERS.keys()

    for extension in available_extensions:

        extension_checker = formats.registries.REGISTERED_FORMAT_CHECKERS[extension]

        if extension_checker(file_name) is True:
            return (extension)


def sanitize_file_format(file_format):

    if re.match(r"^\.*([a-zA-Z\d]+)", file_format) is None:
        raise KeyError("read_structure_step: the file format %s could not be validated" % file_format)

    file_format = file_format.lower()
    
    if file_format.startswith(".") is False:
        file_format = "." + file_format

    return file_format
