from laserfarm import GeotiffWriter
import pathlib
import requests
import time
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--features', action='store' , required='True', dest='features')

arg_parser.add_argument('--param_feature_name', action='store', type=str, required='True', dest='param_feature_name')
arg_parser.add_argument('--param_grafana_base_url', action='store', type=str, required='True', dest='param_grafana_base_url')
arg_parser.add_argument('--param_grafana_token', action='store', type=str, required='True', dest='param_grafana_token')
arg_parser.add_argument('--param_hostname', action='store', type=str, required='True', dest='param_hostname')
arg_parser.add_argument('--param_login', action='store', type=str, required='True', dest='param_login')
arg_parser.add_argument('--param_password', action='store', type=str, required='True', dest='param_password')
arg_parser.add_argument('--param_remote_path_ahn', action='store', type=str, required='True', dest='param_remote_path_ahn')
arg_parser.add_argument('--param_remote_path_root', action='store', type=str, required='True', dest='param_remote_path_root')

args = arg_parser.parse_args()

id = args.id

features = args.features

param_feature_name = args.param_feature_name
param_grafana_base_url = args.param_grafana_base_url
param_grafana_token = args.param_grafana_token
param_hostname = args.param_hostname
param_login = args.param_login
param_password = args.param_password
param_remote_path_ahn = args.param_remote_path_ahn
param_remote_path_root = args.param_remote_path_root

conf_remote_path_targets = pathlib.Path(param_remote_path_root + '/targets')
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_notebook_name = 'Laserfarm_updated'
conf_grafana_verify_ssl = True
conf_local_tmp = pathlib.Path('/tmp')

conf_remote_path_targets = pathlib.Path(param_remote_path_root + '/targets')
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_notebook_name = 'Laserfarm_updated'
conf_grafana_verify_ssl = True
conf_local_tmp = pathlib.Path('/tmp')

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


feature = features

remote_path_geotiffs = pathlib.Path(param_remote_path_ahn).parent / 'geotiffs'

geotiff_export_input = {
    'setup_local_fs': {'tmp_folder': conf_local_tmp.as_posix()},
    'pullremote': conf_remote_path_targets.as_posix(),
    'parse_point_cloud': {},
    'data_split': {'xSub': 1, 'ySub': 1},
    'create_subregion_geotiffs': {'output_handle': 'geotiff'},
    'pushremote': remote_path_geotiffs.as_posix(),
    'cleanlocalfs': {}   
}

writer = GeotiffWriter(input_dir=param_feature_name, bands=param_feature_name,label=param_feature_name).config(geotiff_export_input).setup_webdav_client(conf_wd_opts)
writer.run()
end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='GeoTIFF Export 01-06-22')

import json
filename = "/tmp/remote_path_geotiffs_" + id + ".json"
file_remote_path_geotiffs = open(filename, "w")
file_remote_path_geotiffs.write(json.dumps(remote_path_geotiffs))
file_remote_path_geotiffs.close()
