import pathlib
import sys
from minio import Minio
import pandas as pd
import h5py
import json
import re
import os
import shutil
import subprocess
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_minio_access_key', action='store', type=str, required='True', dest='param_minio_access_key')
arg_parser.add_argument('--param_minio_endpoint', action='store', type=str, required='True', dest='param_minio_endpoint')
arg_parser.add_argument('--param_minio_input_bucket', action='store', type=str, required='True', dest='param_minio_input_bucket')
arg_parser.add_argument('--param_minio_input_prefix', action='store', type=str, required='True', dest='param_minio_input_prefix')
arg_parser.add_argument('--param_minio_secret_key', action='store', type=str, required='True', dest='param_minio_secret_key')
arg_parser.add_argument('--param_minio_secure', action='store', type=str, required='True', dest='param_minio_secure')
arg_parser.add_argument('--param_radar_db_source_name', action='store', type=str, required='True', dest='param_radar_db_source_name')

args = arg_parser.parse_args()

id = args.id


param_minio_access_key = args.param_minio_access_key
param_minio_endpoint = args.param_minio_endpoint
param_minio_input_bucket = args.param_minio_input_bucket
param_minio_input_prefix = args.param_minio_input_prefix
param_minio_secret_key = args.param_minio_secret_key
param_minio_secure = args.param_minio_secure
param_radar_db_source_name = args.param_radar_db_source_name

conf_minio_download_dir = './minio_download_dir' #Set this to something relevant to your machine. I'm uncertain how the VRE handles directories but specify a path to download to.

conf_minio_download_dir = './minio_download_dir' #Set this to something relevant to your machine. I'm uncertain how the VRE handles directories but specify a path to download to.

minioClient = Minio(endpoint = param_minio_endpoint,
                access_key= param_minio_access_key,
                secret_key= param_minio_secret_key,
                secure= bool(param_minio_secure))


list_objects = minioClient.list_objects(bucket_name = param_minio_input_bucket,
                                        prefix = param_minio_input_prefix,
                                        recursive = True)

minioClient.fget_object(param_minio_input_bucket,param_radar_db_source_name, param_radar_db_source_name)
with open(param_radar_db_source_name, mode="r") as f:
    radar_db_json = json.load(f)
    radar_db = {}
for radar_dict in radar_db_json:
    try:
        wmo_code = int(radar_dict.get("wmocode"))
        radar_db.update({wmo_code: radar_dict})
    except Exception:  # Happens when there is for ex. no wmo code.
        pass

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

def gen_output_path(ibed_pvol_file_name):

    """
    Read a file, determine what the path convention is.
    Input is a filename str which is already in the IBED naming convention

    PVOL:       DEASB_pvol_20190215T0000    >   pvol/DE/ASB/2019/02/15
                DEBOO_pvol_20190215T0000    >   pvol/DE/BOO/2019/02/15
                NLHRW_pvol_20190215T0000    >   pvol/NL/HRW/2019/02/15
                UKCHE_pvol_20190215T0000    >   pvol/UK/CHE/2019/02/15
                BEZAV_pvol_20190215T0000    >   pvol/BE/ZAV/2019/02/15
    """

    # dateexpr = r'(\d{8})(T{0,1})(\d{4})'

    # match = re.match(dateexpr,out_pvol_pathibed_pvol_file_name)
    # print(match)

    output_path = "/".join(
        [
            ibed_pvol_file_name[0:2],  # Country
            ibed_pvol_file_name[2:5],  # Radar abbreviation
            ibed_pvol_file_name[11:15],  # Year
            ibed_pvol_file_name[15:17],  # Month
            ibed_pvol_file_name[17:19],  # Day
            "",  # Adding a trailing slash
        ]
    )

    return output_path

    
def translate_wmo_odim(radar_db, wmo_code):
    """"""

    # class FileTranslatorFileTypeError(LookupError):
    #    '''raise this when there's a filetype mismatch derived from h5 file'''

    if not isinstance(wmo_code, int):
        raise ValueError("Expecting a wmo_code [int]")
    else:
        pass

   
    odim_code = (
        radar_db.get(wmo_code).get("odimcode").upper().strip()
    )  # Apparently, people sometimes forget to remove whitespace..
    return odim_code

def extract_wmo_code(in_path):

    with h5py.File(in_path, "r") as f:

        # DWD Specific

        # Main attributes
        what = f["what"].attrs

        # Source block
        source = what.get("source")
        source = source.decode("utf-8")

        # Determine if we are dealing with a WMO code or with an ODIM code set
        # Example from Germany where source block is set as WMO
        # what/source: "WMO:10103"
        # Example from The Netherlands where source block is set as a combination of ODIM and various codes
        # what/source: RAD:NL52,NOD:nlhrw,PLC:Herwijnen
        source_list = source.split(sep=",")

    wmo_code = [string for string in source_list if "WMO" in string]

    # Determine if we had exactly one WMO hit
    if len(wmo_code) == 1:
        wmo_code = wmo_code[0]
        wmo_code = wmo_code.replace("WMO:", "")

    # No wmo code found, most likeley dealing with a dutch radar
    elif len(wmo_code) == 0:
        rad_str = [string for string in source_list if "RAD" in string]

        if len(rad_str) == 1:
            rad_str = rad_str[0]
        else:
            print(
                "Something went wrong with determining the rad_str and it wasnt WMO either, exiting"
            )
            sys.exit(1)
        # Split the rad_str
        rad_str_split = rad_str.split(":")
        # [0] = RAD, [1] = rad code
        rad_code = rad_str_split[1]

        rad_codes = {"NL52": "6356", "NL51": "6234", "NL50": "6260"}

        wmo_code = rad_codes.get(rad_code)

    return int(wmo_code)

def dwd_file_translator(radar_db, in_file):
    class FileTranslatorFileTypeError(LookupError):
        """raise this when there's a filetype mismatch derived from h5 file"""

    # Available codes. Adjust this to load radardb from ../conf/
    wmo_odim_code = {
        "10204": "DEEMD",
        "10103": "DEASB",
        "10169": "DEROS",
        "10132": "DEBOO",
        "10339": "DEHNR",
        "10440": "DEFLD",
        "10629": "DEOFT",
        "10908": "DEFBG",
        "10605": "DENHB",
        "10410": "DEESS",
        "10557": "DENEU",
        "10950": "DEMEM",
        "10873": "DEISN",
        "10832": "DETUR",
        "10780": "DEEIS",
        "10488": "DEDRS",
        "10392": "DEPRO",
        "10356": "DEUMD",
        "06410": "BEJAB",
        "06477": "BEWID",
        "06451": "BEZAV",
        "6356": "NLHRW",
        "6234": "NLDHL",
        "6260": "NLDBL",
        "06194": "DKBOR",
        "06034": "DKSIN",
        "06096": "DKROM",
        "06173": "DKSTE",
        "06103": "DKVIR",
    }

    try:
        wmo_code = extract_wmo_code(in_file)
        odim_code = translate_wmo_odim(radar_db, wmo_code)

        with h5py.File(in_file, "r") as f:

            # DWD Specific

            # Main attributes
            what = f["what"].attrs

            # Date block
            date = what.get("date")
            date = date.decode("utf-8")

            # Time block
            time = what.get("time")
            # time = f['dataset1/what'].attrs['endtime']
            time = time.decode("utf-8")
            hh = time[:2]
            mm = time[2:4]
            ss = time[4:]

            time = time[:-2]  # Do not include seconds
            # File type
            filetype = what.get("object")
            filetype = filetype.decode("utf-8")

            if filetype != "PVOL":
                raise FileTranslatorFileTypeError("File type was NOT pvol")

        name = [odim_code, filetype.lower(), date + "T" + time, str(wmo_code) + ".h5"]
        out_file_name = "_".join(name)

    except Exception as e:
        print(e)
        print("Invalid file, skipping file: {}".format(in_file))
        return None
    # Remove None (None stays when we could not open the file..)

    # out_file_paths = [path.replace(os.path.basename(path),fname) for path,fname in zip(checked_in_file,out_file_name)]
    out_file_path = in_file.replace(os.path.basename(in_file), out_file_name)

    # ibed_out_path = gen_output_path(out_file_name[0])
    ibed_out_path = gen_output_path(out_file_name)

    # out_file_paths = ["/".join(["./out/pvol/",ibed_out_path,fname]) for fname in out_file_name]
    out_file_path = "/".join(["./out/pvol/", ibed_out_path, out_file_name])

    return out_file_path

df = pd.DataFrame()
df['source_pvol_path'] = local_input_file_paths    
df['out_pvol_file_path'] = [dwd_file_translator(radar_db, path) for path in df["source_pvol_path"]] 

def list_unique_dirs(path_list):
    """

    path_list: a list with path strings
    return: a list with unique directories

    """

    unique_dirs = list(set([os.path.dirname(path) for path in path_list]))

    return unique_dirs


unique_dir_pvol = list_unique_dirs(df['out_pvol_file_path'])
gen_output_path(df['out_pvol_file_path'].iloc[0])


def vol2bird(in_file, out_dir, radar_db, add_version=True, add_sector=False):
    # Construct output file
    date_regex = "([0-9]{8})"

    if add_version == True:
        version = "v0-3-20"
        suffix = pathlib.Path(in_file).suffix
        in_file_name = pathlib.Path(in_file).name
        in_file_stem = pathlib.Path(in_file_name).stem
        #
        out_file_name = in_file_stem.replace("pvol", "vp")
        out_file_name = "_".join([out_file_name, version]) + suffix

        # odim = odim_code(out_file_name)
        wmo = extract_wmo_code(in_file)
        odim = translate_wmo_odim(radar_db, wmo)

        datetime = pd.to_datetime(re.search(date_regex, out_file_name)[0])

        ibed_path = "/".join(
            [
                odim[:2],
                odim[2:],
                str(datetime.year),
                str(datetime.month).zfill(2),
                str(datetime.day).zfill(2),
            ]
        )

        out_file = "/".join([out_dir, ibed_path, out_file_name])

        # out_file = "_".join([out_file[:-len(suffix)], version + suffix])

    command = ["vol2bird", in_file, out_file]
    #command = ["/Users/nicolas_noe/vol2bird/opt/vol2bird/bin/vol2bird", in_file, out_file]

    result = subprocess.run(command, stderr=subprocess.DEVNULL)

    # if result.returncode != 0:
    #    print(result)
    #    print("Something went wrong, exitting")
    #    sys.exit(1)
    return [result, in_file, out_file]

for dir_name in unique_dir_pvol:
    os.makedirs(dir_name, exist_ok=True)

for idx, row in df.iterrows():
    shutil.copy(row['source_pvol_path'], row['out_pvol_file_path'])
    
df['out_vp_path'] = [row['out_pvol_file_path'].replace("pvol","vp") for idx, row in df.iterrows()]

unique_dir_vp = list_unique_dirs(df['out_vp_path'])

for dir_name in unique_dir_vp:
    os.makedirs(dir_name, exist_ok=True)

df['v2b_retcode'] = [None] * len(df)
df['out_vp_path'] = [None] * len(df) # This is quite redundant, I'll check this when I'm back. Basically, now we are throwing away our old generated VP paths



input_file_list = []

for idx, row in df.iterrows():
    input_file_list.append(row['out_pvol_file_path'])
    # retcode, input_file, output_file = vol2bird(row['out_pvol_file_path'],
    #          out_dir_vp,
    #          radar_db)
    # # append output file 
    # output_file_list.append(output_file)
    

import json
filename = "/tmp/input_file_list_" + id + ".json"
file_input_file_list = open(filename, "w")
file_input_file_list.write(json.dumps(input_file_list))
file_input_file_list.close()
