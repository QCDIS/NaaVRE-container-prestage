
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




conf_1 = ''
conf_2 = ''
conf_3 = 'def'

out = param_1 + param_2

import json
filename = "/tmp/out_" + id + ".json"
file_out = open(filename, "w")
file_out.write(json.dumps(out))
file_out.close()
