#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# The Chief Editor of Music runs the show.

import sys, os, time, json, logging, re

from ed_melicorum_utils import get_cfg_data, write_roman, write_roman_version
from praedica_min import praedica_min
from incoha import incoha
from lectormelicus.lector_melicus import lege_tabulae_gabc, copy_conv_gabc_vars
from scriptormelicus.scriptor_melicus import write_song_ly, write_title_ly

# /////   Loading internal configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "../../data", "configs.json")) as f:
    configs_data = json.load(f)


def get_opmode_by_id(input_id):
    for o_mode in configs_data["opModes"]:
        if o_mode["id"] == input_id:
            return o_mode
    return None


def get_dialog_string(dialog_key, variables=None):
    raw_string = configs_data["dialog"][dialog_key]
    if (variables is not None) or variables:
        return raw_string.format(variables[0])
    return raw_string


def print_frame(
    textinput,
    large=False,
    light=False,
    extra_space=False,
    show_top=True,
    show_bottom=True,
):
    formatted_input = textinput
    if extra_space:
        formatted_input = "///\n" + textinput + "///\n"

    if show_top:
        print("///============================================================")
    if large:
        print("///")
    print(formatted_input)
    if large:
        print("///")
    if show_bottom:
        if light:
            print("///····························································")
        else:
            print("///------------------------------------------------------------")


def print_intro():
    main_frame_txt = "///   E D I T O R I S      M E L I C O R U M\n"
    main_frame_txt = (
        main_frame_txt
        + f"///\n///------------------------------------------------------------\n"
    )
    main_frame_txt = main_frame_txt + "///\n///   FABRICA SALVADORIS -- MMXXV\n"
    main_frame_txt = main_frame_txt + "///   Salvador Workshop -- 2025\n"
    main_frame_txt = main_frame_txt + f'///\n///   v{configs_data["version"]}'
    print()
    print_frame(main_frame_txt, large=True)
    print()
    print_frame("///   S E R V I C E S      M E N U", large=True)
    print("///")
    for o_mode in configs_data["opModes"]:
        o_mode_text = f'///   < {o_mode["id"]} >  {o_mode["name"]}\n'
        o_mode_text += (
            f"///····························································\n"
        )
        o_mode_text += f'///   {o_mode["desc"]}\n///\n///'
        print_frame(o_mode_text, show_top=False, show_bottom=False)
    print()


# /////   Main Program

print_intro()
opmode_name = ""

try:
    if len(sys.argv) > 1:
        # user has entered arguments. try to parse-
        # script name is the first arg, num value is 2nd
        arg_input = sys.argv[1]
        input_operation_mode = int(arg_input, 10)

        opmode_name = get_opmode_by_id(input_operation_mode)["nameConfirmation"]
        user_input = input(get_dialog_string("actionConfirmation", [opmode_name]))
        if user_input.lower() != "y":
            print(get_dialog_string("exit"))
            sys.exit()
    else:
        # user has not entered arguments.
        u_input_op_mode = input(get_dialog_string("intro"))
        input_operation_mode = int(u_input_op_mode, 10)

        opmode_name = get_opmode_by_id(input_operation_mode)["nameConfirmation"]
        u_input_confirmation = input(
            get_dialog_string("actionConfirmation", [opmode_name])
        )
        if u_input_confirmation.lower() != "y":
            print(get_dialog_string("exit"))
            sys.exit()

except (TypeError, ValueError):
    logging.exception("TypeError / ValueError -- Integer casting probably failed")
    input_operation_mode = None
except BaseException:
    logging.exception("An exception was thrown!")
    input_operation_mode = None

# TODO -- set up "requirements.txt"
# TODO -- SET UP CODE DOCUMENTATION TOOLS

print(get_dialog_string("performingAction1"))
time.sleep(0.75)
print(get_dialog_string("performingAction2", [opmode_name]))
time.sleep(1.5)

cfg_data = get_cfg_data()


def to_conv_ly_paths(source_doc):
    cleaned_path = source_doc["path"].replace(".gabc", ".ly")
    return os.path.join(cfg_data["output_dir_ly_data"], cleaned_path)


input_documents = cfg_data["documents"]

if input_operation_mode == 1:

    # ------------------------------------
    # ARRANGE / COMPOSE

    for in_doc in input_documents:
        conv_gabc_docs = map(to_conv_ly_paths, in_doc["sourceDocs"])

        # ---------
        # Templates

        template_title_path = os.path.join(
            cfg_data["data_templates_dir"], "ed_melicorum_title.ly"
        )
        template_gt_all_path = os.path.join(
            cfg_data["data_templates_dir"], "bookpart_gtr_all.ly"
        )
        template_gt_accomp_path = os.path.join(
            cfg_data["data_templates_dir"], "bookpart_gtr_accomp.ly"
        )
        template_gt_solo_path = os.path.join(
            cfg_data["data_templates_dir"], "bookpart_gtr_solo.ly"
        )

        gabc_file_meta = lege_tabulae_gabc(in_doc["id"], in_doc["sourceDocs"])

        # ------------------
        # LilyPond variables

        vars_vocals_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_vocals.ly"
        )
        vars_lyrics_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_lyrics.ly"
        )
        vars_gt_comp_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_gt_comp.ly"
        )
        vars_gt_solo_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_gt_solo.ly"
        )

        # ----------------------
        # LilyPond bookpart sets

        bookparts_gt_all = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_bkpts_gt_all.ly"
        )
        bookparts_gt_accomp = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_bkpts_gt_accomp.ly"
        )
        bookparts_gt_solo = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_bkpts_gt_solo.ly"
        )

        # ------------------------
        # Document sections, parts

        title_gt_all_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_title_gt_all.ly"
        )
        title_gt_accomp_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_title_gt_accomp.ly"
        )
        title_gt_solo_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_title_gt_solo.ly"
        )

        # ------------------------
        # Preparing to write to files

        clear_fpaths = [
            vars_vocals_path,
            vars_lyrics_path,
            vars_gt_comp_path,
            vars_gt_solo_path,
            bookparts_gt_all,
            bookparts_gt_accomp,
            bookparts_gt_solo,
            title_gt_all_path,
            title_gt_accomp_path,
            title_gt_solo_path,
        ]
        for fpath in clear_fpaths:
            with open(fpath, "w") as ofile:
                ofile.write("\n")  # clearing text

        # ------------------------
        # Writing output

        doc_data = {
            "DocTitle": in_doc["name"],
            "DocTitleLat": in_doc["nameLat"],
            "DocPart": "Complete Guitar Version",
            "DocPartLat": "Versio Cuncta Citharœdi",
            "DocVersion": in_doc["version"],
            "DocVersionLat": write_roman_version(in_doc["version"]),
        }
        write_title_ly(title_gt_all_path, template_title_path, doc_data)

        doc_data["DocPart"] = "Guitar Accompanist Version"
        doc_data["DocPartLat"] = "Versio Citharœdi Auxiliaris"
        write_title_ly(title_gt_accomp_path, template_title_path, doc_data)

        doc_data["DocPart"] = "Guitar Soloist Version"
        doc_data["DocPartLat"] = "Versio Citharœdi Primi"
        write_title_ly(title_gt_solo_path, template_title_path, doc_data)

        # Copying LY vars, writing song part
        for cgd_idx, conv_gabc_doc in enumerate(conv_gabc_docs, start=1):
            filename_slug = os.path.basename(conv_gabc_doc).replace(".ly", "")
            filename_slug = filename_slug.replace("-", " ")
            filename_slug = filename_slug.title().replace(" ", "")
            filename_slug = re.sub(
                "[0-9]+", lambda match: write_roman(int(match.group())), filename_slug
            )

            meta_key = f"{in_doc['id']}_{cgd_idx}"

            transpose_key = copy_conv_gabc_vars(
                filename_slug,
                conv_gabc_doc,
                vars_vocals_path,
                vars_lyrics_path,
                vars_gt_comp_path,
                vars_gt_solo_path,
            )

            # can't be moved here yet :(
            # gabc_file_meta = lege_tabulae_gabc(in_doc["id"], in_doc["sourceDocs"])

            song_data = {
                "Title": gabc_file_meta[meta_key]["name"],
                "Subtitle": gabc_file_meta[meta_key]["office-part"],
                "Instrument": f"Modus {write_roman(int(gabc_file_meta[meta_key]["mode"]))}",
                "Composer": gabc_file_meta[meta_key]["book"],
                "Arranger": f"descr. {gabc_file_meta[meta_key]["transcriber"]}",
                "Vocals": f"Vocals{filename_slug}",
                "Lyrics": f"Lyrics{filename_slug}",
                "GuitarAccomp": f"GtrComp{filename_slug}",
                "GuitarSolo": f"GtrSolo{filename_slug}",
                "LyricsLink": f"vox{filename_slug}".lower(),
                "TransposeKey": f"{transpose_key}",
                "Database": "GregoBase",
            }

            write_song_ly(bookparts_gt_all, template_gt_all_path, song_data)
            write_song_ly(bookparts_gt_accomp, template_gt_accomp_path, song_data)
            write_song_ly(bookparts_gt_solo, template_gt_solo_path, song_data)

        # Create arrangement / composition sheets
        incoha(in_doc["path"], in_doc["version"])
        incoha(in_doc["partPaths"][0], in_doc["version"])
        incoha(in_doc["partPaths"][1], in_doc["version"])

elif input_operation_mode == 2:

    # ------------------------------------
    # DRAFT ARRANGEMENTS (PREVIEW)

    print("NOTE: Drafts not available!")

elif input_operation_mode == 3:

    # ------------------------------------
    # PUBLISH ARRANGEMENTS

    print("NOTE: Publishing not available!")

else:
    print(get_dialog_string("error"))
