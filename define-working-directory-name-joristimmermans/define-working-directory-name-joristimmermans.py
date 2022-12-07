
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




working_directory_name = 'OVP_test_pynb39_20220717'

import json
filename = "/tmp/working_directory_name_" + id + ".json"
file_working_directory_name = open(filename, "w")
file_working_directory_name.write(json.dumps(working_directory_name))
file_working_directory_name.close()
