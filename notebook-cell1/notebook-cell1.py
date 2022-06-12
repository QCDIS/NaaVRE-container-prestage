from laserfarm import Retiler
import requests
import laspy
from laserfarm.remote_utils import list_remote
from laserfarm.remote_utils import get_wdclient
import copy
import time
from laserfarm import GeotiffWriter
import pathlib
from laserfarm import DataProcessing
import json
from webdav3.client import Client
import numpy as np
import os
import fnmatch
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_apply_filter_value', action='store', type=str, required='True', dest='param_apply_filter_value')
arg_parser.add_argument('--param_attribute', action='store', type=str, required='True', dest='param_attribute')
arg_parser.add_argument('--param_feature_name', action='store', type=str, required='True', dest='param_feature_name')
arg_parser.add_argument('--param_filter_type', action='store', type=str, required='True', dest='param_filter_type')
arg_parser.add_argument('--param_grafana_base_url', action='store', type=str, required='True', dest='param_grafana_base_url')
arg_parser.add_argument('--param_grafana_token', action='store', type=str, required='True', dest='param_grafana_token')
arg_parser.add_argument('--param_laz_compression_factor', action='store', type=str, required='True', dest='param_laz_compression_factor')
arg_parser.add_argument('--param_max_filesize', action='store', type=str, required='True', dest='param_max_filesize')
arg_parser.add_argument('--param_max_x', action='store', type=str, required='True', dest='param_max_x')
arg_parser.add_argument('--param_max_y', action='store', type=str, required='True', dest='param_max_y')
arg_parser.add_argument('--param_min_x', action='store', type=str, required='True', dest='param_min_x')
arg_parser.add_argument('--param_min_y', action='store', type=str, required='True', dest='param_min_y')
arg_parser.add_argument('--param_n_tiles_side', action='store', type=str, required='True', dest='param_n_tiles_side')
arg_parser.add_argument('--param_tile_mesh_size', action='store', type=str, required='True', dest='param_tile_mesh_size')
arg_parser.add_argument('--param_validate_precision', action='store', type=str, required='True', dest='param_validate_precision')

args = arg_parser.parse_args()

id = args.id


param_apply_filter_value = args.param_apply_filter_value
param_attribute = args.param_attribute
param_feature_name = args.param_feature_name
param_filter_type = args.param_filter_type
param_grafana_base_url = args.param_grafana_base_url
param_grafana_token = args.param_grafana_token
param_laz_compression_factor = args.param_laz_compression_factor
param_max_filesize = args.param_max_filesize
param_max_x = args.param_max_x
param_max_y = args.param_max_y
param_min_x = args.param_min_x
param_min_y = args.param_min_y
param_n_tiles_side = args.param_n_tiles_side
param_tile_mesh_size = args.param_tile_mesh_size
param_validate_precision = args.param_validate_precision




                    

                    

conf_remote_path_root = pathlib.Path('/webdav')
conf_remote_path_ahn = pathlib.Path('/webdav/ahn')
conf_remote_path_split = pathlib.Path('/webdav/split')
conf_remote_path_retiled = pathlib.Path('/webdav/retiled/')
conf_remote_path_norm = pathlib.Path('/webdav/norm/')
conf_remote_path_targets = pathlib.Path('/webdav/targets')
conf_local_tmp = pathlib.Path('/tmp')




conf_wd_opts = { 'webdav_hostname': param_hostname, 'webdav_login': param_login, 'webdav_password': param_password}



conf_notebook_name = ''
conf_grafana_verify_ssl = True

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
    

def save_chunk_to_laz_file(in_filename, 
                           out_filename, 
                           offset, 
                           n_points):
    """Read points from a LAS/LAZ file and write them to a new file."""
    
    points = np.array([])
    
    with laspy.open(in_filename) as in_file:
        with laspy.open(out_filename, 
                        mode="w", 
                        header=in_file.header) as out_file:
            in_file.seek(offset)
            points = in_file.read_points(n_points)
            out_file.write_points(points)
    return len(points)

def split_strategy(filename, max_filesize):
    """Set up splitting strategy for a LAS/LAZ file."""
    with laspy.open(filename) as f:
        bytes_per_point = (
            f.header.point_format.num_standard_bytes +
            f.header.point_format.num_extra_bytes
        )
        n_points = f.header.point_count
    n_points_target = int(
        max_filesize * int(param_laz_compression_factor) / bytes_per_point
    )
    stem, ext = os.path.splitext(filename)
    return [
        (filename, f"{stem}-{n}{ext}", offset, n_points_target)
        for n, offset in enumerate(range(0, n_points, n_points_target))
    ]


start = int(round(time.time() * 1000))

client = Client(conf_wd_opts)
client.mkdir(conf_remote_path_split.as_posix())


remote_path_split = conf_remote_path_split

file = laz_files

client.download_sync(remote_path=os.path.join(conf_remote_path_ahn,file), local_path=file)
inps = split_strategy(file, int(param_max_filesize))
for inp in inps:
    save_chunk_to_laz_file(*inp)
client.upload_sync(remote_path=os.path.join(conf_remote_path_split,file), local_path=file)

for f in os.listdir('.'):
    if not f.endswith('.LAZ'):
        continue
    os.remove(os.path.join('.', f))
    
split_laz_files = laz_files

end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='split big files 01-60-22')

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
remote_path_retiled
tiles = [t.strip('/') for t in list_remote(get_wdclient(conf_wd_opts), conf_remote_path_retiled.as_posix())
         if fnmatch.fnmatch(t, 'tile_*_*/')]

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

remote_path_norm
norm_tiles = [t.strip('/') for t in list_remote(get_wdclient(conf_wd_opts), conf_remote_path_norm.as_posix())
         if fnmatch.fnmatch(t, 'tile_*_*.laz')]

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


features = [param_feature_name]

tile_mesh_size = float(param_tile_mesh_size)

grid_feature = {
    'min_x': float(param_min_x),
    'max_x': float(param_max_x),
    'min_y': float(param_min_y),
    'max_y': float(param_max_y),
    'n_tiles_side': int(param_n_tiles_side)
}

feature_extraction_input = {
    'setup_local_fs': {'tmp_folder': conf_local_tmp.as_posix()},
    'pullremote': conf_remote_path_norm.as_posix(),
    'load': {'attributes': [param_attribute]},
    'normalize': 1,
    'apply_filter': {
        'filter_type': param_filter_type, 
        'attribute': param_attribute,
        'value': [int(param_apply_filter_value)]#ground surface (2), water (9), buildings (6), artificial objects (26), and unclassified (1)
    },
    'generate_targets': {
        'tile_mesh_size' : tile_mesh_size,
        'validate' : True,
        'validate_precision': float(param_validate_precision),
        **grid_feature
    },
    'extract_features': {
        'feature_names': features,
        'volume_type': 'cell',
        'volume_size': tile_mesh_size
    },
    'export_targets': {
        'attributes': features,
        'multi_band_files': False
    },
    'pushremote': conf_remote_path_targets.as_posix(),
}    

t = norm_tiles
stem, _ = os.path.splitext(t)
idx = [int(el) for el in (stem.split('_')[1:])]
processing = DataProcessing(t, tile_index=idx,label=stem).config(feature_extraction_input).setup_webdav_client(conf_wd_opts)
processing.run()

end = int(round(time.time() * 1000))
send_annotation(start=start,end=end,message='Feature Extraction 01-06-22')

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

remote_path_geotiffs = conf_remote_path_ahn.parent / 'geotiffs'

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
print(remote_path_geotiffs)

