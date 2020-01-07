"""
Implementation of the reader for XYZ files using OpenBabel
"""

import os
import seamm
import seamm_util
from read_structure_step.errors import MopError
from read_structure_step.formats.registries import register_reader
from ..which import which
from .find_mopac import find_mopac
import re


def _find_charge(regex, input_file):
    text = re.search(regex, input_file)
    if text is not None:
#        return "CHARGE={}".format(text.group(2))
        return text.group(2)

#def _find_charge(regex, f):
#    data = f.read()
#    text = re.search(regex, data)
#    f.seek(0)
#    if text is not None:
#        return "CHARGE={}".format(text.group(2))


def _find_standard(regex, input_file):
    text = re.search(regex, input_file)
    if text is not None:
        return text.group(0)

#def _find_standard(regex, f):
#    data = f.read()
#    text = re.search(regex, data)
#    f.seek(0)
#    if text is not None:
#        return text.group(0)


#def _find_symmetry(regex, input_file):
#    split = input_file.split("\n")
#    block = []
#    for line in split:
#        text = re.search(regex, line)
#        if text is not None:
#            block.append(text.group(0))
#    if len(block) > 0:
#        return ''.join(block)

def _find_field(regex, input_file):
    text = re.search(regex, input_file)
    if text is not None:
        return (text.group(2), text.group(5), text.group(8)) 

#def _find_symmetry(regex, f):
#    block = []
#    for line in f:
#        text = re.search(regex, line)
#        if text is not None:
#            block.append(text.group(0))
#    f.seek(0)
#    if len(block) > 0:
#        return ''.join(block)

def _find_open(regex, input_file):
    text = re.search(regex, input_file)
    if text is not None:
        return (text.group(2), text.group(3))

extras = {
            "structure":
                {
                    "net_charge":
                    {
                        "regex": r"(CHARGE=)([\+\-]?\d)",
                        "find": _find_charge,
                        "value": None,
                    },
                    "field":
                    {
                        "regex": r"(FIELD=\()([-+]?\d+(\.\d+(e[-+]\d+)?)?\,)([-+]?\d+(\.\d+(e[-+]\d+)?)?\,)([-+]?\d+(\.\d+(e[-+]\d+)?)?)\)",
                        "find": _find_field,
                        "value": None,
                    },
                    #"symmetry":
                    #{
                    #    "regex": r"^(\s*\d+\s*)+$",
                    #    "find": _find_symmetry,
                    #    "value": None,
                    #},
                    "open":
                    {
                        "regex": r"(OPEN\()(\d+)\,\s*(\d+)\)",
                        "find": _find_open,
                        "value": None,
                    },
                },
            "methods":
                {
                    "UHF":
                    {
                        "regex": r"UHF",
                        "find": _find_standard,
                        "value": None,
                    },
                    "PULAY":
                    {
                        "regex": r"PULAY",
                        "find": _find_standard,
                        "value": None,
                    },
                },

        }

obabel_error_identifiers = ['0 molecules converted']

@register_reader('.mop')
def load_mop(file_name):

    with open(file_name, "r") as f:
        input_file = f.read()
        for k, v in extras.items():
            for ko, vo in v.items():
                regex = extras[k][ko]['regex']
                extras[k][ko]["value"] = vo["find"](regex, input_file)


#        for k, v in extras.items():
#            for ko, vo in v.items():
#                regex = extras[k][ko]['regex']
#                extras[k][ko]["value"] = vo["find"](regex, f)

    try:

        obabel_exe = which('obabel')
        local = seamm.ExecLocal()

        result = local.run(
            cmd=[
                obabel_exe, '-f 1', '-l 1', '-imop', file_name, '-omol', '-x3'
            ]
        )
        for each_error in obabel_error_identifiers:
            if each_error in result['stderr']:
                raise MopError(
                    'OpenBabel: Could not read input file. %s' % result
                )

        mol = result['stdout']

        structure = seamm_util.molfile.to_seamm(mol, extras["structure"])

        return structure

    except MopError:

        mopac_exe = find_mopac()

        if mopac_exe is None:
            raise FileNotFoundError('The MOPAC executable could not be found')

        with open(file_name, "r") as f:
            data = f.read()

            hamiltonians = [
                'AM1',
                'MNDO',
                'MNDOD',
                'PM3',
                'PM6',
                'PM6-D3',
                'PM6-DH+',
                'PM6-DH2',
                'PM6-DH2X',
                'PM6-D3H4',
                'PM6-D3H4X',
                'PM7',
                'PM7-TS',
                'RM1',
            ]

            for hamiltonian in hamiltonians:
                if hamiltonian in data:
                    data = data.replace(hamiltonian, "0SCF", 1)
                    break

        tmp_file = os.path.dirname(file_name) + "/_0SCFTemp.mop"

        with open(tmp_file, "w") as f:
            f.write(data)

        local = seamm.ExecLocal()
        local.run(cmd=[mopac_exe, tmp_file])


        output_file = os.path.dirname(file_name) + '/_0SCFTemp.out'

        obabel_exe = which('obabel')
        local = seamm.ExecLocal()
    
        result = local.run(
            cmd=[
                obabel_exe, '-f 1', '-l 1', '-imoo', output_file, '-omol',
                '-x3'
            ]
        )

        os.remove(tmp_file)
        os.remove(output_file)

        for each_error in obabel_error_identifiers:
            if each_error in result['stderr']:
                raise MopError(
                    'OpenBabel: Could not read input file. %s' % result
                )

        mol = result['stdout']

        structure = seamm_util.molfile.to_seamm(mol, extras["structure"])

        return structure
