import os
import json
from collections import OrderedDict


def write_roman(num):

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= r * x
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])


def write_roman_version(ver_str):
    out_str = ""
    separator = "."
    semver_parts = ver_str.split(separator)

    for pt_idx, part in enumerate(semver_parts):
        if pt_idx > 0:
            out_str = out_str + separator
        if part == "0":
            out_str = out_str + "nulla"
        else:
            part_num = int(part)
            out_str = out_str + f"{write_roman(part_num).lower()}"

    return out_str


file_dir = os.path.dirname(os.path.realpath(__file__))
repo_dir = os.path.join(file_dir, "../../")
input_dir = os.path.join(repo_dir, "input")
internal_dir = os.path.join(repo_dir, "internal")
output_dir = os.path.join(repo_dir, "output")


def get_cfg_data():
    cfg_data = {
        "gabctk_script_fname": "gabctk.py",
        "repo_dir": repo_dir,
        "input_dir": os.path.join(repo_dir, "input"),
        "internal_dir": os.path.join(repo_dir, "internal"),
        "output_dir": os.path.join(repo_dir, "output"),
        "cfg_filename": "edimeli.config.json",
        "input_meta_filename": "metadata.json",
    }
    cfg_data["cfg_filepath"] = os.path.join(cfg_data["repo_dir"], cfg_data["cfg_filename"])
    cfg_data["gabctk_log_filepath"] = os.path.join(cfg_data["internal_dir"], 'gabctk_log.txt')
    cfg_data["lilypond_log_filepath"] = os.path.join(cfg_data["internal_dir"], 'lilypond_log.txt')

    with open(f"{cfg_data['cfg_filepath']}", "r") as file:
        cfg_json = json.load(file)
        cfg_data["gabctk_dir"] = os.path.join(
            repo_dir, cfg_json["paths"]["gabctkDirectory"]
        )
        cfg_data["output_dir_ly_data"] = os.path.join(
            repo_dir, cfg_json["paths"]["outputDirectoryLyData"]
        )
        cfg_data["output_dir_ly"] = os.path.join(
            repo_dir, cfg_json["paths"]["outputDirectoryLy"]
        )
        cfg_data["output_dir_pdf"] = os.path.join(
            repo_dir, cfg_json["paths"]["outputDirectoryPdf"]
        )
        cfg_data["data_templates_dir"] = os.path.join(
            repo_dir, cfg_json["paths"]["dataTemplatesDirectory"]
        )

    return cfg_data


def get_repo_dir():
    return repo_dir


def print_char_line(char, num_chars):
    out = ""
    for x in range(num_chars):
        out = out + char
    return out


def print_frame(str, data_dict, other_dict):
    char_div1 = "="
    char_div2 = "-"
    char_div3 = "·"

    spacing = 2
    dash_margin = 6
    totwidth = (spacing + dash_margin) * 2 + len(str)

    heading_dash_unit = print_char_line(char_div1, dash_margin)
    footer_line = print_char_line(char_div2, totwidth)
    divider_line = print_char_line(char_div3, totwidth)

    output = f"\n\n{heading_dash_unit} {str} {heading_dash_unit}\n"

    for dkey, dvalue in data_dict.items():
        output = output + f"{dkey}: {dvalue}\n"

    output = output + "\n"

    for okey, ovalue in other_dict.items():
        output = output + f"{okey}: {ovalue}\n"

    output = output + f"{footer_line}\n\n"

    print(output)
