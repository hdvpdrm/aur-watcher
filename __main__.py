import aurwatcher
import sys
import requests
import json

if __name__ == "__main__":
    args = aurwatcher.parse_arguments()
    response = requests.get(aurwatcher.compute_request(args))
    if response.status_code != 200:
        print("request failed with code {}".format(response.status_code))
        sys.exit(1)


    converted = dict(json.loads(response.text))["results"]
    found_packages = [aurwatcher.extract_required_info(x,args["s"]) for x in converted]
    aurwatcher.print_result(found_packages,args["o"])
    
