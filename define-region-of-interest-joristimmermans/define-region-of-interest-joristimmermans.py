
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




roi = 'POLYGON ((5.163574 52.382529, 5.163574 52.529813, 5.493164 52.529813, 5.493164 52.382529, 5.163574 52.382529))'
roi_grid = 'EPSG:4326'

import json
filename = "/tmp/roi_" + id + ".json"
file_roi = open(filename, "w")
file_roi.write(json.dumps(roi))
file_roi.close()
filename = "/tmp/roi_grid_" + id + ".json"
file_roi_grid = open(filename, "w")
file_roi_grid.write(json.dumps(roi_grid))
file_roi_grid.close()
