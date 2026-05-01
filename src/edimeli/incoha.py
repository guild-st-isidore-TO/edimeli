#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import subprocess
from pathlib import Path

from .utils import print_frame, get_cfg_data

# ---------------
# CONFIGURATION

cfg_data = get_cfg_data()

Path(cfg_data["output_dir_ly"]).mkdir(parents=True, exist_ok=True)
Path(cfg_data["output_dir_pdf"]).mkdir(parents=True, exist_ok=True)
logfile_path = cfg_data["lilypond_log_filepath"]

# --------------
# USING LILYPOND


def incoha(doc_path, doc_version):
    """Drafts arrangement / composition sheets"""
    print(f"> incoha()")
    print(f"    doc_path: {doc_path}")
    print(f"    doc_version: {doc_version}")
    out_file_name = os.path.basename(doc_path).replace(".ly", f"-v{doc_version}")

    drafts_data = {}
    drafts_data["in_file_path"] = os.path.join(cfg_data["input_dir"], doc_path)
    drafts_data["out_file_path"] = os.path.join(
        cfg_data["output_dir_pdf"], out_file_name
    )

    cmd_backend_opt = 'ps' # 'ps', 'cairo', or 'svg'
    cmd_string = f"lilypond -dbackend={cmd_backend_opt} -l DEBUG -o {drafts_data['out_file_path']} {drafts_data['in_file_path']} &> {logfile_path}"

    print_frame("USING LILYPOND", cfg_data, drafts_data)

    try:
        # logfile = open(logfile_path, "w")
        # retcode = subprocess.call(cmd_string, shell=True, stdout=logfile)
        retcode = subprocess.call(cmd_string, shell=True)
        if retcode < 0:
            print("> Lilypond process terminated by signal", -retcode, file=sys.stderr)
        else:
            print("> Lilypond process returned", retcode, file=sys.stderr)
    except OSError as e:
        print("> Execution failed:", e, file=sys.stderr)
