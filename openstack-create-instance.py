#!/usr/bin/env python

import os, sys, getopt
from novaclient.client import Client

def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hn:i:w:",["name=","network=","image="])
    except getopt.GetoptError:
        print 'openstack-create-instance.py --name <instance_name> --network <network_name> --image <image_name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'openstack-create-instance.py --name <instance_name> --network <network_name> --image <image_name>'
            sys.exit()
        elif opt in ("-n", "--name"):
            instance_name = arg
        elif opt in ("-w", "--network"):
            network_name = arg
        elif opt in ("-i", "--image"):
            image_name = arg
        else:
            print 'openstack-create-instance.py --name <instance_name> --network <network_name> --image <image_name>'
            sys.exit(3)


    if 'network_name' not in locals() or 'image_name' not in locals() or 'instance_name' not in locals():
        print 'openstack-create-instance.py --name <instance_name> --network <network_name> --image <image_name>'
        sys.exit(4)


    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    try:
        image = nova_client.images.find(name=image_name)
        flavor = nova_client.flavors.find(name="m1.tiny")
        net = nova_client.networks.find(label=network_name)
        nics = [{'net-id': net.id}]
        instance = nova_client.servers.create(name=instance_name, image=image,
            flavor=flavor, nics=nics)
    finally:
        print("Instance "+instance_name+" created")

if __name__ == "__main__":
    main(sys.argv[1:])
