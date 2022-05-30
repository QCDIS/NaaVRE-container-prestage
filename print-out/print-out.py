import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--output_file_list', action='store' , required='True', dest='output_file_list')


args = arg_parser.parse_args()

id = args.id

output_file_list = args.output_file_list




print(output_file_list)

