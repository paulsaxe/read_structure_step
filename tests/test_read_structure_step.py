#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `read_structure_step` package."""

import pytest  # noqa: F401
import read_structure_step  # noqa: F401
from . import build_filenames

def test_single_mol2():

    mol2_file = build_filenames.build_data_filename('test.mol2')
    mol2_parsed = read_structure_step.ReadStructure()._read(mol2_file)
