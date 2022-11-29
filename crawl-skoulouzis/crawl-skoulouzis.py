
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')

arg_parser.add_argument('--list_of_req', action='store', type=list, required='True', dest='list_of_req')

arg_parser.add_argument('--param_username', action='store', type=str, required='True', dest='param_username')

args = arg_parser.parse_args()

id = args.id

list_of_req = args.list_of_req

param_username = args.param_username



def send(resp,param_username):
    print(resp)
    
for req in list_of_req:
    
    resp = req + 'a'
    send(resp,param_username)

