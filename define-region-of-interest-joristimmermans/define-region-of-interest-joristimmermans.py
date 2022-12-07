
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




roi = 'POLYGON ((5.163574 52.382529, 5.163574 52.529813, 5.493164 52.529813, 5.493164 52.382529, 5.163574 52.382529))'
spatial_resolution = 20


import json
filename = "/tmp/roi_" + id + ".json"
file_roi = open(filename, "w")
file_roi.write(json.dumps(roi))
file_roi.close()
