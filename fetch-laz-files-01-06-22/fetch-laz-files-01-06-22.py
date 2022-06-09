import requests
from laserfarm.remote_utils import get_wdclient
import time
import pathlib
from laserfarm.remote_utils import list_remote
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_grafana_base_url', action='store', type=str, required='True', dest='param_grafana_base_url')
arg_parser.add_argument('--param_grafana_token', action='store', type=str, required='True', dest='param_grafana_token')
arg_parser.add_argument('--param_hostname', action='store', type=str, required='True', dest='param_hostname')
arg_parser.add_argument('--param_login', action='store', type=str, required='True', dest='param_login')
arg_parser.add_argument('--param_password', action='store', type=str, required='True', dest='param_password')

args = arg_parser.parse_args()

id = args.id


param_grafana_base_url = args.param_grafana_base_url
param_grafana_token = args.param_grafana_token
param_hostname = args.param_hostname
param_login = args.param_login
param_password = args.param_password

conf_notebook_name = ''
conf_grafana_verify_ssl = True
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_remote_path_ahn = pathlib.Path('/webdav/ahn')

conf_notebook_name = ''
conf_grafana_verify_ssl = True
conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}
conf_remote_path_ahn = pathlib.Path('/webdav/ahn')

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

laz_files = [f for f in list_remote(get_wdclient(conf_wd_opts), conf_remote_path_ahn.as_posix())
             if f.lower().endswith('.laz')]
end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='Fetch Laz Files 01-06-22')

import json
filename = "/tmp/laz_files_" + id + ".json"
file_laz_files = open(filename, "w")
file_laz_files.write(json.dumps(laz_files))
file_laz_files.close()
