#!/usr/bin/env python

import sys
import requests
import json
import pprint
import os

OS_AUTH_URL=os.environ.get('OS_AUTH_URL')
OS_TENANT_ID=os.environ.get('OS_TENANT_ID')
OS_TENANT_NAME=os.environ.get('OS_TENANT_NAME')
OS_USERNAME=os.environ.get('OS_USERNAME')
OS_PASSWORD=os.environ.get('OS_PASSWORD')

if OS_AUTH_URL == None or OS_TENANT_ID == None or OS_TENANT_NAME == None or OS_USERNAME == None or OS_PASSWORD == None :
    print "You need to source your environment variable from your OpenStack RC file"
    sys.exit(1)
#print "OS_AUTH_URL="+OS_AUTH_URL
#print "OS_USERNAME="+OS_USERNAME
#print "OS_PASSWORD="+OS_PASSWORD


def post_request(URL,DATA):
    try:
        response = requests.post(
            url=URL,
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(DATA)
        )
        data = json.loads(response.text)
        return data
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_request(URL, TOKEN):
    try:
        response = requests.get(
            url=URL,
            headers={
                "Content-Type": "application/json",
                "X-Auth-Token": TOKEN
            }
        )
        data = json.loads(response.text)
        return data
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

pp=pprint.PrettyPrinter(indent=4)

token=post_request(OS_AUTH_URL+"/tokens",{
                "auth": {
                    "passwordCredentials": {
                        "username": OS_USERNAME,
                        "password": OS_PASSWORD
                    },
                    "tenantName": OS_TENANT_NAME,
                }
            })["access"]["token"]["id"]
#print "Token="+token

# Get Compute Service URL
endpoint_list=get_request(OS_AUTH_URL.replace('v2.0','v3')+"/endpoints", token)["endpoints"]
service_list=get_request(OS_AUTH_URL.replace('v2.0','v3')+"/services", token)["services"]
s=(item for item in service_list if item["name"] == "Compute Service").next()
e=(e["url"] for e in endpoint_list if e["service_id"]==s["id"]).next()
OS_NOVA_URL=e
#print "OS_NOVA_URL="+OS_NOVA_URL

net_list=get_request(OS_NOVA_URL.replace("$(tenant_id)s",OS_TENANT_ID)+"/os-networks",token)["networks"]
tenant_list=get_request(OS_AUTH_URL.replace('v2.0','v3')+"/projects",token)["projects"]

print "Network_ID\t\t\t\tNetwork_Name\tNetwork_Address\tProject_ID\t\t\t\tProject_Name"
for net in net_list:
    l = list(t["name"] for t in tenant_list if t["id"]==net["project_id"])
    if not net["project_id"]:
        print net["id"]+"\t"+net["label"]+"\t"+net["cidr"]+"\t"+"!!! FREE !!!"
    else:
        if l==[]:
            print net["id"]+"\t"+net["label"]+"\t"+net["cidr"]+"\t"+net["project_id"]+"\t"+"!!! DELETED !!!"
        else:
            print net["id"]+"\t"+net["label"]+"\t"+net["cidr"]+"\t"+net["project_id"]+"\t"+l[0]

