#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from pathlib import Path

from ed_melicorum_utils import print_frame, get_cfg_data


# ---------------
# CONFIGURATION

cfg_data = get_cfg_data()

Path(cfg_data["output_dir_ly"]).mkdir(parents=True, exist_ok=True)
Path(cfg_data["output_dir_pdf"]).mkdir(parents=True, exist_ok=True)


# --------------
# USING LILYPOND


def praedica_min(main_doc):
    """Publishes preview versions"""
    ## TODO: Turn this into an actual publishing doc, not just a "blank sheets" copy

    cfg_data["in_file_path"] = f"{cfg_data['doc_dir']}/{main_doc}"
    cfg_data["out_file_path"] = f"{cfg_data['output_dir_pdf']}"
    cfg_data["cmd_string"] = (
        f"lilypond -l VERBOSE -o {cfg_data['out_file_path']} {cfg_data['in_file_path']}"
    )

    print_frame("USING LILYPOND", cfg_data, {})

    try:
        retcode = subprocess.call(cfg_data["cmd_string"], shell=True)
        if retcode < 0:
            print("Child process terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child process returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
