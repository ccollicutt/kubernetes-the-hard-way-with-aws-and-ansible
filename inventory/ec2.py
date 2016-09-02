#!/usr/bin/env python

from boto import ec2
import json
import sys
import os

inventory = {}
inventory['_meta'] = { 'hostvars': {} }
inventory['all'] = []


#
# Make boto connection
#

try:
  aws_region =  os.environ['AWS_REGION']
except:
  print "ERROR: The AWS_REGION environment variable must be set"
  sys.exit(1)

# Make the connection to AWS API
try:
  ec2conn = ec2.connect_to_region(aws_region)
except:
  print "ERROR: Unable to connect to AWS"
  sys.exit(1)

# Run through all the instances
reservations = ec2conn.get_all_instances()
instances = [i for r in reservations for i in r.instances]
for i in instances:

  # Check if the host has a name, if not we don't care about it anyways
  try:
    host_name = i.tags['Name']
  except:
    host_name = False

  if i.state == "running" and host_name:

    # Check for a public IP, if non use the private IP
    if i.ip_address:
      ip =  i.ip_address
    else:
      ip =  i.private_ip_address

    # kubernetes role...
    try:
      krole = "tag_krole_" + i.tags['krole']
    except: 
      krole = None

    if krole != None:
      try:
        inventory[krole].append(host_name)
      except:
        inventory[krole] = []    
        inventory[krole].append(host_name)

      # Only want hosts with a krole, ignore all others
      inventory['all'].append(host_name)
      inventory['_meta']['hostvars'][host_name] = {}
      inventory['_meta']['hostvars'][host_name]['ansible_ssh_host'] = ip

print(json.dumps(inventory, indent=4))
