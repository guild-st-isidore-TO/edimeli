import argparse
import pathlib
import sys, os, time, json, logging, re

from edimeli.utils import get_cfg_data, write_roman, write_roman_version
from incoha import incoha
from lectormelicus.lector_melicus import lege_tabulae_gabc, copy_conv_gabc_vars
from scriptormelicus.scriptor_melicus import write_song_ly, write_title_ly

cfg_data = get_cfg_data()

input_dir_data = pathlib.Path(cfg_data["input_dir"])
input_dir_list = list(input_dir_data.iterdir())
input_dir_project_dirs = list(filter(lambda item: item.is_dir(), input_dir_list))
input_dir_projects = list(map(lambda path_obj: path_obj.name, input_dir_project_dirs))

script_desc = "Transforms models in the given input project"


def get_intermediate_ly_paths(source_doc):
    cleaned_path = source_doc["path"].replace(".gabc", ".ly")
    return os.path.join(cfg_data["output_dir_ly_data"], cleaned_path)


def translate_voice():
    parser = argparse.ArgumentParser(description=script_desc)
    args = parser.parse_args()

    print("\n----------------------------------------------------------------\n")

    print(f"> TRANSLATE VOICE")
    print(f">")

    # input_documents = cfg_data["documents"]

    # ------------------------------------
    # ARRANGE / COMPOSE

    for proj_id in input_dir_projects:
        proj_meta_path = os.path.join(
            cfg_data["input_dir"], proj_id, cfg_data["input_meta_filename"]
        )
        in_meta = {}
        with open(proj_meta_path) as f:
            in_meta = json.load(f)

        in_doc = dict()
        in_doc.update(in_meta)
        in_doc.update({"other_prop1": "dxfadfg", "other_prop2": "khjskfsd"})

        intermediate_ly_paths = map(get_intermediate_ly_paths, in_doc["sourceDocs"])

        # ---------
        # Templates

        template_title_path = os.path.join(
            cfg_data["data_templates_dir"], "ed_melicorum_title.ly"
        )
        template_gt_all_path = os.path.join(
            cfg_data["data_templates_dir"], "bookpart_gtr_all.ly"
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

        # ------------------------
        # Document sections, parts

        title_gt_all_path = os.path.join(
            cfg_data["output_dir_ly"], f"{in_doc['id']}_title_gt_all.ly"
        )

        # ------------------------
        # Preparing to write to files

        clear_fpaths = [
            vars_vocals_path,
            vars_lyrics_path,
            vars_gt_comp_path,
            vars_gt_solo_path,
            bookparts_gt_all,
            # bookparts_gt_accomp,
            # bookparts_gt_solo,
            title_gt_all_path,
            # title_gt_accomp_path,
            # title_gt_solo_path,
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

        # doc_data["DocPart"] = "Guitar Accompanist Version"
        # doc_data["DocPartLat"] = "Versio Citharœdi Auxiliaris"
        # write_title_ly(title_gt_accomp_path, template_title_path, doc_data)

        # doc_data["DocPart"] = "Guitar Soloist Version"
        # doc_data["DocPartLat"] = "Versio Citharœdi Primi"
        # write_title_ly(title_gt_solo_path, template_title_path, doc_data)

        # Copying LY vars, writing song part
        for cgd_idx, conv_gabc_doc in enumerate(intermediate_ly_paths, start=1):
            filename_slug = os.path.basename(conv_gabc_doc).replace(".ly", "")
            filename_slug = filename_slug.replace("-", " ")
            filename_slug = filename_slug.title().replace(" ", "")
            filename_slug = re.sub(
                "[0-9]+",
                lambda match: write_roman(int(match.group())),
                filename_slug,
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
            # write_song_ly(bookparts_gt_accomp, template_gt_accomp_path, song_data)
            # write_song_ly(bookparts_gt_solo, template_gt_solo_path, song_data)

        # Create arrangement / composition sheets
        incoha(in_doc["path"], in_doc["version"])
        incoha(in_doc["partPaths"][0], in_doc["version"])
        incoha(in_doc["partPaths"][1], in_doc["version"])

    print("\n----------------------------------------------------------------\n")


if __name__ == "__translate_voice__":
    translate_voice()
