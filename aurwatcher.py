#!/usr/bin/env python3
#Usage example: aurwatcher p=emacs

import sys
import argparse
from functools import reduce
import subprocess
from getch import read_single_char

def print_help():
    options = '''
    arch-watcher looks for packages in AUR or in official repository.\n\n

    ./arch-watcher p=emacs s=[aur|off] o=[pt|ip]\n
    p - package name                  \n
    s - source(aur xor official repo) \n
    o - output mode(plain text xor inner pager) plain text is choosen by default\n
    '''
    print(options)
    
def process_mode(mode_value):
    if mode_value not in ("pt","ip"):
        print("incorrect value for ouput mode {}".format(mode_value))
        print_help()
        sys.exit(1)

    return False if mode_value == "pt" else True

def prepare_arguments():
    parser = argparse.ArgumentParser(prog="aurwatcher",description="script looks for packages in AUR or in official repository.")
    parser.add_argument("p",help="defines package-name substring to look for")
    parser.add_argument("-s","--source",help="choose source of finding.",choices=["AUR","off"])
    parser.add_argument("-o","--output",help="choose output mode(plain text xor inner pager)",choices=["pt","ip"])
    return parser.parse_args()

def parse_arguments():
    args = vars(prepare_arguments())
    result = {}
    result["o"] = "pt" if args["output"] is None else args["output"]
    result["s"] = "AUR" if args["source"] is None else args["source"]
    result["p"] =args["p"]
    return result
    
def compute_request(args):
    source = args["s"]
    package = args["p"]

    if source.lower() not in ("off","aur"):
        print("{} is unknown source".format(source))
        sys.exit(1)

    if source == "aur":
        return "https://aur.archlinux.org/rpc/?v=5&type=search&arg={}".format(package)
    else:
        return  "https://archlinux.org/packages/search/json/?q={}".format(package)


def get_source_related_keys_list(source):
    if source == "aur":
        return ("Name","Description","Maintainer","URL","Version","OutOfData")
    else:
        return ("pkgname","pkgdesc","packager","repo","arch","url")
    
def extract_required_info(response_result,source):
    data = {}
    for key,value in response_result.items():
        if key in get_source_related_keys_list(source):
            data[key] = value
    return data


def print_result(response, paging_mode=False):
    for id,item in enumerate(response):
        print("found item #{}".format(id))
        print("-"*40)
        for k in item.keys():
            print("{}:{}".format(k,item[k]))
        print("-"*40)
        if paging_mode:
            if read_single_char() == 'q':
                sys.exit(0)
            else:
                subprocess.run(["clear"])

    
