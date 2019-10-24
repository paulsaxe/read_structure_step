#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `read_structure_step` package."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames


@pytest.mark.parametrize('file_name', [1, [], {}, 1.0])
def test_read_filename_type(file_name):

    with pytest.raises(TypeError):
        read_structure_step.read(file_name)

def test_empty_filename():
    
    with pytest.raises(NameError):
        read_structure_step.read('')

def test_unregistered_readers():
    
    with pytest.raises(KeyError):

        xyz_file = build_filenames.build_data_filename('spc.xyz')
        read_structure_step.read(xyz_file, extension='.mp3')

@pytest.mark.parametrize("extension", [None, ".xyz", "xyz", "XYZ"])
def test_single_xyz_file(extension):

    xyz_file = build_filenames.build_data_filename("spc.xyz") 
    parsed_xyz = read_structure_step.read(xyz_file, extension=extension) 
    
    assert len(parsed_xyz["atoms"]["elements"]) == 3
    assert all(atom in ["O", "H", "H"] for atom in parsed_xyz["atoms"]["elements"])
    assert len(parsed_xyz["atoms"]["coordinates"]) == 3
    assert all(len(point) == 3 for point in parsed_xyz["atoms"]["coordinates"])
    assert len(parsed_xyz["bonds"]) == 2
    assert any(bond == (2, 1, 'single') for bond in parsed_xyz["bonds"])
    assert any(bond == (3, 1, 'single') for bond in parsed_xyz["bonds"])
