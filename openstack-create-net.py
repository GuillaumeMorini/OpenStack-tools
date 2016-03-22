#!/usr/bin/env python

import os, sys, getopt
from neutronclient.v2_0 import client

def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    d['region_name'] = os.environ['OS_REGION_NAME']
    return d

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hn:i:",["name=","cidr="])
    except getopt.GetoptError:
        print 'openstack-create-net.py -n <network_name> -i <cidr_address>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'openstack-create-net.py -n <network_name> -i <cidr_address>'
            sys.exit()
        elif opt in ("-n", "--name"):
            network_name = arg
        elif opt in ("-i", "--cidr"):
            cidr = arg
        else:
            print 'openstack-create-net.py -n <network_name> -i <cidr_address>'
            sys.exit(3)


    if 'network_name' not in locals() or 'cidr' not in locals():
        print 'openstack-create-net.py -n <network_name> -i <cidr_address>'
        sys.exit(4)


    credentials = get_credentials()
    neutron = client.Client(**credentials)
    try:
        body_sample = {'network': {'name': network_name,
          'admin_state_up': True}}

        netw = neutron.create_network(body=body_sample)
        net_dict = netw['network']
        network_id = net_dict['id']
        print('Network %s created' % network_id)

        body_create_subnet = {'subnets': [{'cidr': cidr,
            'ip_version': 4, 'network_id': network_id}]}

        subnet = neutron.create_subnet(body=body_create_subnet)
        print('Created subnet %s' % subnet)
    finally:
        print("Execution completed")

if __name__ == "__main__":
    main(sys.argv[1:])
