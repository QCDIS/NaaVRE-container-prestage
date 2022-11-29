
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--l', action='store', type=list, required='True', dest='l')

arg_parser.add_argument('--param_user', action='store', type=str, required='True', dest='param_user')

args = arg_parser.parse_args()

id = args.id

l = args.l

param_user = args.param_user


for i in l: 
    print(param_user)
    print(i)

