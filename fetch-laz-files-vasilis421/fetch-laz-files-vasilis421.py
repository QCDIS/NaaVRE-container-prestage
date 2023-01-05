from laserfarm.remote_utils import get_wdclient
from laserfarm.remote_utils import list_remote
import pathlib

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id



conf_hostname = ''
conf_password = ''
conf_remote_path_ahn =  '/webdav/pointcloud' + '/ahn'
conf_login = ''

conf_hostname = ''
conf_password = ''
conf_remote_path_ahn =  '/webdav/pointcloud' + '/ahn'
conf_login = ''
conf_wd_opts = { 'webdav_hostname': conf_hostname, 'webdav_login': conf_login, 'webdav_password': conf_password}
laz_files = [f for f in list_remote(get_wdclient(conf_wd_opts), pathlib.Path(conf_remote_path_ahn).as_posix())
             if f.lower().endswith('.laz')]

import json
filename = "/tmp/laz_files_" + id + ".json"
file_laz_files = open(filename, "w")
file_laz_files.write(json.dumps(laz_files))
file_laz_files.close()
