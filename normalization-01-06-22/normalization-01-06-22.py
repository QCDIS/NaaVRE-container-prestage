import json
import pathlib
from laserfarm import DataProcessing
import requests
import time
import copy
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--tiles', action='store' , required='True', dest='tiles')

arg_parser.add_argument('--param_grafana_base_url', action='store', type=str, required='True', dest='param_grafana_base_url')
arg_parser.add_argument('--param_grafana_token', action='store', type=str, required='True', dest='param_grafana_token')
arg_parser.add_argument('--param_hostname', action='store', type=str, required='True', dest='param_hostname')
arg_parser.add_argument('--param_login', action='store', type=str, required='True', dest='param_login')
arg_parser.add_argument('--param_password', action='store', type=str, required='True', dest='param_password')

args = arg_parser.parse_args()

id = args.id

tiles = args.tiles

param_grafana_base_url = args.param_grafana_base_url
param_grafana_token = args.param_grafana_token
param_hostname = args.param_hostname
param_login = args.param_login
param_password = args.param_password

conf_remote_path_retiled = pathlib.Path('/webdav/retiled/')
conf_remote_path_norm = pathlib.Path('/webdav/norm/')
conf_local_tmp = pathlib.Path('/tmp')
conf_grafana_verify_ssl = True
conf_notebook_name = 'Laserfarm_updated'
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}

conf_remote_path_retiled = pathlib.Path('/webdav/retiled/')
conf_remote_path_norm = pathlib.Path('/webdav/norm/')
conf_local_tmp = pathlib.Path('/tmp')
conf_grafana_verify_ssl = True
conf_notebook_name = 'Laserfarm_updated'
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}

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


tiles

remote_path_norm = str(conf_remote_path_norm)

normalization_input = {
    'setup_local_fs': {'tmp_folder': conf_local_tmp.as_posix()},
    'pullremote': conf_remote_path_retiled.as_posix(),
    'load': {'attributes': 'all'},
    # Filter out artifically high points - give overflow error when writing
    'apply_filter': {'filter_type':'select_below',
                     'attribute': 'z',
                     'threshold': 10000.},  # remove non-physically heigh points
    'normalize': 1,
    'clear_cache' : {},
    'pushremote': conf_remote_path_norm.as_posix(),
}

with open('normalize.json', 'w') as f:
    json.dump(normalization_input, f)
    

tile = tiles
normalization_input_ = copy.deepcopy(normalization_input)
normalization_input_['export_point_cloud'] = {'filename': '{}.laz'.format(tile),'overwrite': True}
dp = DataProcessing(tile, label=tile).config(normalization_input_).setup_webdav_client(conf_wd_opts)
dp.run()

end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='normalization 01-06-22')

import json
filename = "/tmp/remote_path_norm_" + id + ".json"
file_remote_path_norm = open(filename, "w")
file_remote_path_norm.write(json.dumps(remote_path_norm))
file_remote_path_norm.close()
