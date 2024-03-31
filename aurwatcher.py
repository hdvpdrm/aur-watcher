#!/usr/bin/env python3
#Usage example: aurwatcher p=emacs

import sys
import argparse
import subprocess
from getch import read_single_char

def prepare_arguments():
    '''create CLI parser'''
    parser = argparse.ArgumentParser(prog="aurwatcher",
                                     description="script looks for packages in AUR or in official repository.")
    parser.add_argument("p",
                        help="defines package-name substring to look for")
    parser.add_argument("-s","--source",
                        help="choose source of finding.",
                        choices=["AUR","off"])
    parser.add_argument("-o",
                        "--output",
                        help   ="choose output mode(plain text xor inner pager)",
                        choices=["pt","ip"])
    return parser.parse_args()

def parse_arguments():
    '''This function is weird, I know, but it is required, because it's convert passed arguments to
       old format i used before started to use argparse.

       Note: i think it can be refactored.'''
    args = vars(prepare_arguments())
    result = {}
    result["o"] = "pt" if args["output"] is None else args["output"]
    result["s"] = "AUR" if args["source"] is None else args["source"]
    result["p"] =args["p"]
    return result

def compute_request(args):
    '''generate rpc-request'''
    source = args["s"]
    package = args["p"]

    if source.lower() not in ("off","aur"):
        print("{} is unknown source".format(source))
        sys.exit(1)

    if source == "AUR":
        return "https://aur.archlinux.org/rpc/?v=5&type=search&arg={}".format(package)
    else:
        return  "https://archlinux.org/packages/search/json/?q={}".format(package)


def get_source_related_keys_list(source):
    '''since response is big json file, then we need only specific keys'''
    if source == "AUR":
        return ("Name","Description","Maintainer","URL","Version","OutOfData")
    else:
        return ("pkgname","pkgdesc","packager","repo","arch","url")
    
def extract_required_info(response_result,source):
    '''response is json-file and this function filters it to return only required data'''
    data = {}
    for key,value in response_result.items():
        if key in get_source_related_keys_list(source):
            data[key] = value
    return data

def print_result(response, paging_mode=False):
    '''print output as plain text or using "inner pager"'''
    paging_mode = True if paging_mode == "ip" else False
    
    for i,item in enumerate(response):
        print("found item #{}".format(i))
        print("-"*40)
        for k in item.keys():
            print("{}:{}".format(k,item[k]))
        print("-"*40)
        if paging_mode:
            if read_single_char() == 'q':
                sys.exit(0)
            else:
                subprocess.run(["clear"]) #check isn't required here, because clear won't fail

    
