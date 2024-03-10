#!/usr/bin/env python3
#Usage example: aurwatcher p=emacs

import sys
from functools import reduce
import subprocess

def print_help():
    options = '''
    arch-watcher looks for packages in AUR or in official repository.\n\n

    ./arch-watcher p=emacs s=[aur|off]\n
    p - package name                  \n
    s - source(aur xor official repo) \n
    o - output mode(plain text xor inner pager)\n
    '''
    print(options)
    

def parse_arguments():
    '''returns the hash-table of arguments'''
    
    #at least there is only one argument - the script name
    if len(sys.argv) == 1:
        print("error: not enough arguments")
        print_help()
        sys.exit(1)
    
    table = {} #key is argument name and value is argument's value

    #p - package
    #s - source
    available_keys = "ps"

    for arg in sys.argv[1:]:
        #try to parse argument
        try:
            left, right = arg.split("=")
        except ValueError:
            print("incorrect format of argument! it should be a=b")
            print_help()
            sys.exit(1)

        #key should exist as available key and it must not be added already
        if left in available_keys and left not in table.keys():
            table[left] = right
        else:
            print("key is used already or doesn't exist!")
            print_help()
            sys.exit(1)
    
    return table

def compute_request(args):
    source = args["s"]
    package = args["p"]

    if source not in ("off","aur"):
        print("{} is unknown source".format(source))
        sys.exit(1)

    if source == "aur":
        return "https://aur.archlinux.org/rpc/?v=5&type=search&arg={}".format(package)
    else:
        return  "https://archlinux.org/packages/search/json/?q={}".format(package)


def get_source_related_keys_list(source):
    if source == "aur":
        return ("Name","Description","Maintainer")
    else:
        return ("pkgname","pkgdesc","packager","repo","arch","url")
    
def extract_required_info(response_result,source):
    data = {}
    for key,value in response_result.items():
        if key in get_source_related_keys_list(source):
            data[key] = value
    return data


def __print_all(response):
    for id,item in enumerate(response):
        print("found item #{}".format(id))
        print("-"*40)
        for k in item.keys():
            print("{}:{}".format(k,item[k]))
        print("-"*40)

def print_result(response,use_pager=False):
    __print_all(response)
    
