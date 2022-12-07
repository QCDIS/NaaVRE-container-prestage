
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




start_time_as_string = '2008-04-16'
stop_time_as_string = '2008-04-20'

time_step = 5 # in days

import json
filename = "/tmp/time_step_" + id + ".json"
file_time_step = open(filename, "w")
file_time_step.write(json.dumps(time_step))
file_time_step.close()
filename = "/tmp/stop_time_as_string_" + id + ".json"
file_stop_time_as_string = open(filename, "w")
file_stop_time_as_string.write(json.dumps(stop_time_as_string))
file_stop_time_as_string.close()
filename = "/tmp/start_time_as_string_" + id + ".json"
file_start_time_as_string = open(filename, "w")
file_start_time_as_string.write(json.dumps(start_time_as_string))
file_start_time_as_string.close()
