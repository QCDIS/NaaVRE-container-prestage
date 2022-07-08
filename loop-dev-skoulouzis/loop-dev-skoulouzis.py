import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')
args = arg_parser.parse_args()

id = args.id


arg_parser.add_argument('--laz_files', action='store' , required='True', dest='laz_files')


laz_files = args.laz_files




for file in laz_files:
    print(file)
    

