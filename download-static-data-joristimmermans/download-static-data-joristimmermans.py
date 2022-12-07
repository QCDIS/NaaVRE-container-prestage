from multiply_data_access import DataAccessComponent
from vm_support.utils import set_permissions
from vm_support.sym_linker import create_sym_links
import os

import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--roi', action='store', type=str, required='True', dest='roi')

arg_parser.add_argument('--roi_grid', action='store', type=str, required='True', dest='roi_grid')

arg_parser.add_argument('--start_time_as_string', action='store', type=str, required='True', dest='start_time_as_string')

arg_parser.add_argument('--stop_time_as_string', action='store', type=str, required='True', dest='stop_time_as_string')

arg_parser.add_argument('--working_dir', action='store', type=str, required='True', dest='working_dir')


args = arg_parser.parse_args()
print(args)

id = args.id

roi = args.roi
roi_grid = args.roi_grid
start_time_as_string = args.start_time_as_string
stop_time_as_string = args.stop_time_as_string
working_dir = args.working_dir




def get_static_data(data_access_component: DataAccessComponent, roi: str, roi_grid: str, start_time: str,
                    stop_time: str, emulation_directory: str, dem_directory: str):
    create_dir(emulation_directory)
    create_dir(dem_directory)

    rg = roi_grid
    if roi_grid == 'none':
        rg = None
    
    print('Retrieving emulators ...')
    emu_urls = data_access_component.get_data_urls(roi, start_time, stop_time, 'ISO_MSI_A_EMU,ISO_MSI_B_EMU', rg)
    set_permissions(emu_urls)
    create_sym_links(emu_urls, emulation_directory)
    
    print('Retrieving DEM ...')
    dem_urls = data_access_component.get_data_urls(roi, start_time, stop_time, 'Aster_DEM', rg)
    set_permissions(dem_urls)
    create_sym_links(dem_urls, dem_directory)
    print('Done retrieving static data')

def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except:
        print(dir)
    return
emulators_directory = '{}/emulators'.format(working_dir)
dem_directory = '{}/dem'.format(working_dir)

data_access_component = DataAccessComponent()

get_static_data(data_access_component=data_access_component, roi=roi,
                start_time=start_time_as_string, stop_time=stop_time_as_string, 
          emulation_directory=emulators_directory, dem_directory=dem_directory, roi_grid=roi_grid)

