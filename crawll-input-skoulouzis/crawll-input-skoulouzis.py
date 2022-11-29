
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()

id = args.id




list_of_req = ['a','b','c']

import json
filename = "/tmp/list_of_req_" + id + ".json"
file_list_of_req = open(filename, "w")
file_list_of_req.write(json.dumps(list_of_req))
file_list_of_req.close()
