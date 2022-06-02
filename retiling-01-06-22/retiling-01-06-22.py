import pathlib
from laserfarm import Retiler
import requests
import time
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--split_laz_files', action='store' , required='True', dest='split_laz_files')

arg_parser.add_argument('--param_grafana_base_url', action='store', type=str, required='True', dest='param_grafana_base_url')
arg_parser.add_argument('--param_grafana_token', action='store', type=str, required='True', dest='param_grafana_token')
arg_parser.add_argument('--param_hostname', action='store', type=str, required='True', dest='param_hostname')
arg_parser.add_argument('--param_login', action='store', type=str, required='True', dest='param_login')
arg_parser.add_argument('--param_max_x', action='store', type=str, required='True', dest='param_max_x')
arg_parser.add_argument('--param_max_y', action='store', type=str, required='True', dest='param_max_y')
arg_parser.add_argument('--param_min_x', action='store', type=str, required='True', dest='param_min_x')
arg_parser.add_argument('--param_min_y', action='store', type=str, required='True', dest='param_min_y')
arg_parser.add_argument('--param_n_tiles_side', action='store', type=str, required='True', dest='param_n_tiles_side')
arg_parser.add_argument('--param_password', action='store', type=str, required='True', dest='param_password')

args = arg_parser.parse_args()

id = args.id

split_laz_files = args.split_laz_files

param_grafana_base_url = args.param_grafana_base_url
param_grafana_token = args.param_grafana_token
param_hostname = args.param_hostname
param_login = args.param_login
param_max_x = args.param_max_x
param_max_y = args.param_max_y
param_min_x = args.param_min_x
param_min_y = args.param_min_y
param_n_tiles_side = args.param_n_tiles_side
param_password = args.param_password

conf_remote_path_retiled = pathlib.Path('/webdav/retiled/')
conf_local_tmp = pathlib.Path('/tmp')
conf_grafana_verify_ssl = True
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_notebook_name = 'Laserfarm_updated'
conf_remote_path_split = pathlib.Path('/webdav/split')

conf_remote_path_retiled = pathlib.Path('/webdav/retiled/')
conf_local_tmp = pathlib.Path('/tmp')
conf_grafana_verify_ssl = True
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_notebook_name = 'Laserfarm_updated'
conf_remote_path_split = pathlib.Path('/webdav/split')

def send_annotation(start=None,end=None,message=None,tags=None):
    if not tags:
        tags = []
    
    tags.append(conf_notebook_name)
    
    headers = {
        'Accept':'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+param_grafana_token
    }
    
    data ={
      "time":start,
      "timeEnd":end,
      "created": end,
      "tags":tags,
      "text": message
    }
    resp = requests.post(param_grafana_base_url+'/api/annotations',verify=conf_grafana_verify_ssl,headers=headers,json=data)
    
    
start = int(round(time.time() * 1000))
remote_path_retiled = str(conf_remote_path_retiled)

grid_retile = {
    'min_x': float(param_min_x),
    'max_x': float(param_max_x),
    'min_y': float(param_min_y),
    'max_y': float(param_max_y),
    'n_tiles_side': int(param_n_tiles_side)
}


retiling_input = {
    'setup_local_fs': {'tmp_folder': conf_local_tmp.as_posix()},
    'pullremote': conf_remote_path_split.as_posix(),
    'set_grid': grid_retile,
    'split_and_redistribute': {},
    'validate': {},
    'pushremote': conf_remote_path_retiled.as_posix(),
    'cleanlocalfs': {}
}


    
file = split_laz_files
retiler = Retiler(file.replace('"',''),label=file).config(retiling_input).setup_webdav_client(conf_wd_opts)
retiler_output = retiler.run()

end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='Retiling 01-06-22')

import json
filename = "/tmp/remote_path_retiled_" + id + ".json"
file_remote_path_retiled = open(filename, "w")
file_remote_path_retiled.write(json.dumps(remote_path_retiled))
file_remote_path_retiled.close()
