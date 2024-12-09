#!/usr/bin/env python3

import subprocess, sys
import argparse

'''
OPS445 Assignment 2
Program: duim.py
Author: "Joanne Kuang"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading.
I understand that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Description: ops445 Assignment 2b

Date: 11-21-2024
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    parser.add_argument("-H", "--human-readable", action="store_true", help="ouput size readable format")
    # check the docs for an argparse option to store this as a boolean.
    # add argument for "target". set number of args to 1.
    parser.add_argument("target", nargs="?", default=".")
    args = parser.parse_args()
    return args


def percent_to_graph(percent: int, total_chars: int) -> str:
    "returns a string: eg. '##  ' for 50 if total_chars == 4"
    total =  int((percent / 100) * total_chars)
    return '=' * total + ' ' * (total_chars - total)
    pass

def call_du_sub(location: str) -> list:
    "use subprocess to call `du -d 1 + location`, rtrn raw list"
    subprocess_to_call = ["du", "-d", "1", location]

    try:
        subproc = subprocess.Popen(subprocess_to_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = subproc.communicate()

        if stderr:
            print("Error when running the du command: " + stderr.strip())
            return []

        return stdout.strip().split("\n")

    except except_error as eerror:
        print("Error occured")
        return []

def create_dir_dict(raw_dat: list) -> dict:
    "get list from du_sub, return dict {'directory': 0} where 0 is size"
    dictionary = {}
    for item_key in raw_dat:
        parts = item_key.split("\t", 1)
        dictionary[parts[1]] = int(parts[0])
    return dictionary

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    target_direct = args.target

    try:
        raw_data = call_du_sub(target_direct)
        info = create_dir_dict(raw_data)

    except execept_error as eerror:
        print("Error couldnt get data: " + args.target)
        sys.exit(1)

    # get total size
    total_size = sum(info.values())

    for pathtofile, size in info.values():

    perc = (size / total_size) * 100 if total_size > 0 else 0
    graph = perctograph(perc, args.length)

    green = "\033[92m"
    light_blue = "\033[94m"
    reset = "\033[0m"

    colour_bar = green + graph + reset
    colour = light_blue + pathtofile + reset

    if args.human-readable:
        size_str = human_read(size)
        total_str = human_read(total_size)
    else:
        size_str = str(size) + " B"
        total_str = str(total_str) " B" 

    # print the result
    print("Total: {:>3.0f}% [{}] {}\t {}".format(perc, colour_bar, size_str, colour))

    print("Total: {} {}".format(total_str, args.target))
