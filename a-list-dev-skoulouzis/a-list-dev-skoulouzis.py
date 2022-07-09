import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_a', action='store', type=int, required='True', dest='param_a')

args = arg_parser.parse_args()

id = args.id


param_a = args.param_a



print(param_a)
laz_files = ['1','2','3']

import json
filename = "/tmp/laz_files_" + id + ".json"
file_laz_files = open(filename, "w")
file_laz_files.write(json.dumps(laz_files))
file_laz_files.close()
