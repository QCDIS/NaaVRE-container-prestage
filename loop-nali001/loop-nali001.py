
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--l', action='store', type=list, required='True', dest='l')


args = arg_parser.parse_args()

id = args.id

l = args.l



for i in l: 
    print(i)

