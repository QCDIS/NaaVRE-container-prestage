from minio import Minio
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--conf_minio_access_key', action='store' , type=str , required='True', dest='conf_minio_access_key')
arg_parser.add_argument('--conf_minio_endpoint', action='store' , type=str , required='True', dest='conf_minio_endpoint')
arg_parser.add_argument('--conf_minio_secret_key', action='store' , type=str , required='True', dest='conf_minio_secret_key')
arg_parser.add_argument('--conf_minio_secure', action='store' , type=str , required='True', dest='conf_minio_secure')


args = arg_parser.parse_args()

id = args.id

conf_minio_access_key = args.conf_minio_access_key
conf_minio_endpoint = args.conf_minio_endpoint
conf_minio_secret_key = args.conf_minio_secret_key
conf_minio_secure = args.conf_minio_secure


conf_minio_input_bucket = 'lifewatchin'
conf_minio_input_prefix = 'NL/DHL/2018/10/03'
conf_minio_download_dir = './minio_download_dir' #Set this to something relevant to your machine. I'm uncertain how the VRE handles directories but specify a path to download to.

conf_minio_input_bucket = 'lifewatchin'
conf_minio_input_prefix = 'NL/DHL/2018/10/03'
conf_minio_download_dir = './minio_download_dir' #Set this to something relevant to your machine. I'm uncertain how the VRE handles directories but specify a path to download to.

minioClient = Minio(endpoint = conf_minio_endpoint,
                access_key= conf_minio_access_key,
                secret_key= conf_minio_secret_key,
                secure= conf_minio_secure)

list_objects = minioClient.list_objects(bucket_name = conf_minio_input_bucket,
                                        prefix = conf_minio_input_prefix,
                                        recursive = True)
local_input_file_paths = []
for list_object in list_objects:
    # Return object_name as str
    object_name = list_object.object_name
    # append object name (file name) to download dir
    local_file_name = "{}/{}".format(conf_minio_download_dir,object_name)
    # fget (file get) the object
    minioClient.fget_object(
        bucket_name= list_object.bucket_name,
        object_name=list_object.object_name,
        file_path=local_file_name)
    # append the full file path to the file path list, for future useage
    local_input_file_paths.append(local_file_name)
        

import json
filename = "/tmp/local_input_file_paths_" + id + ".json"
file_local_input_file_paths = open(filename, "w")
file_local_input_file_paths.write(json.dumps(local_input_file_paths))
file_local_input_file_paths.close()
