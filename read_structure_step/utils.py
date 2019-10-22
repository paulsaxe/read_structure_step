import os
from . import formats


def guess_extension(file_name, with_file_name=False):

    if with_file_name is True:
        (root, ext) = os.path.splitext(file_name)
        return ext.lower()


    available_extensions = formats.registries.REGISTERED_FORMAT_CHECKERS.keys()

    for extension in available_extensions:

        extension_checker = formats.registries.REGISTERED_FORMAT_CHECKERS[extension]

        if extension_checker(file_name) is True:
            return (extension)
