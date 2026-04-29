#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
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


def incoha(doc_path, doc_version):
    """Drafts arrangement / composition sheets"""
    out_file_name = os.path.basename(doc_path).replace(".ly", f"-v{doc_version}")
    drafts_data = {}
    drafts_data["in_file_path"] = f"{cfg_data['doc_dir']}/{doc_path}"
    drafts_data["out_file_path"] = f"{cfg_data['output_dir_pdf']}/{out_file_name}"

    drafts_data["cmd_string"] = (
        f"lilypond -l VERBOSE -o {drafts_data['out_file_path']} {drafts_data['in_file_path']}"
    )

    print_frame("USING LILYPOND", cfg_data, drafts_data)

    try:
        retcode = subprocess.call(drafts_data["cmd_string"], shell=True)
        if retcode < 0:
            print("Child process terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child process returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
