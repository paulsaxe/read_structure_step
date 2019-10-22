import os
import seamm
import seamm_util
from read_structure_step.errors import XYZError
from read_structure_step.formats.registries import register_reader

obabel_error_identifiers= ['0 molecules converted']

@register_reader('.xyz')
def load_mol2(file_name):
        obabel_exe = _which('obabel') 
        local = seamm.ExecLocal()

        result = local.run(
             cmd=[obabel_exe, '-ixyz', file_name, '-omol', '-x3']
        )
        for each_error in obabel_error_identifiers:
            if each_error in result['stderr']:
                raise XYZError('OpenBabel: Could not read input file. %s' % result)

        mol = result['stdout']

        structure = seamm_util.molfile.to_seamm(mol)

        return structure

def _which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None
