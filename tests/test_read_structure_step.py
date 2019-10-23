#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `read_structure_step` package."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames

def test_single_mol2():

    mol2_file = build_filenames.build_data_filename('test.mol2')
    mol2_parsed = read_structure_step.read(mol2_file)

def test_single_xyz():

    xyz_file = build_filenames.build_data_filename('spc.xyz')
    xyz_parsed = read_structure_step.read(xyz_file)


def test_single_pdb():

    pdb_file = build_filenames.build_data_filename('hydrolase.pdb')
    pdb_parsed = read_structure_step.read(pdb_file)
