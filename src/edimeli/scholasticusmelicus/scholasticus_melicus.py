#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# The Scholar of Music knows all (relevant) things.

import os
from pathlib import Path

from ed_melicorum_utils import print_frame, get_cfg_data

# ---------------
# CONFIGURATION

file_dir = os.path.dirname(os.path.realpath(__file__))
cfg_data = get_cfg_data()
print_frame("WIP - SCHOLASTICUS MELICUS", cfg_data, {})
