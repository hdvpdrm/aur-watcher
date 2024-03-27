import aurwatcher
import sys
import requests
import json
import os

if __name__ == "__main__":
    #read getch.py to see the reason
    if os.name != "posix":
        print("Sorry! This script won't run on non-posix system!")
        system.exit(1)
    
    args = aurwatcher.parse_arguments()

    response = requests.get(aurwatcher.compute_request(args))
    if response.status_code != 200:
        print("request failed with code {}".format(response.status_code))
        sys.exit(1)


    converted = dict(json.loads(response.text))["results"]
    found_packages = [aurwatcher.extract_required_info(x,args["s"]) for x in converted]
    aurwatcher.print_result(found_packages,args["o"])
    
