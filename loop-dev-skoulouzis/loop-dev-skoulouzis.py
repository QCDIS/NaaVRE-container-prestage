import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--laz_files', action='store' , required='True', dest='laz_files')


args = arg_parser.parse_args()

id = args.id

laz_files = args.laz_files




for file in laz_files:
    print(file)
    

