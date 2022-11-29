
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()

id = args.id




l = ['a', 'b', 'c']

import json
filename = "/tmp/l_" + id + ".json"
file_l = open(filename, "w")
file_l.write(json.dumps(l))
file_l.close()
