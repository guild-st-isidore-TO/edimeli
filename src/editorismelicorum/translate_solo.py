import argparse
import os

root_dir = os.path.join(os.path.dirname(__file__), "..", "..")
input_dir = os.path.join(root_dir, "input")
output_dir = os.path.join(root_dir, "output")

script_desc = "Transforms models in the given input project"


def translate_solo():

    parser = argparse.ArgumentParser(description=script_desc)
    args = parser.parse_args()

    print("\n----------------------------------------------------------------\n")

    print(f"> Test content")

    print("\n----------------------------------------------------------------\n")


if __name__ == "__translate_solo__":
    translate_solo()
