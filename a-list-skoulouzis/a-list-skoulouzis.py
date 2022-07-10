import pathlib
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_a', action='store', type=str, required='True', dest='param_a')
arg_parser.add_argument('--param_username', action='store', type=str, required='True', dest='param_username')

args = arg_parser.parse_args()

id = args.id


param_a = args.param_a
param_username = args.param_username

conf_remote_path_split = pathlib.Path(conf_remote_path_root + '/split_'+param_username)
conf_remote_path_ahn = conf_remote_path_root + '/ahn'

conf_remote_path_split = pathlib.Path(conf_remote_path_root + '/split_'+param_username)
conf_remote_path_ahn = conf_remote_path_root + '/ahn'

print(param_a)
print(conf_remote_path_split)
print(conf_remote_path_ahn)
laz_files = ['1','2','3']

import json
filename = "/tmp/laz_files_" + id + ".json"
file_laz_files = open(filename, "w")
file_laz_files.write(json.dumps(laz_files))
file_laz_files.close()
