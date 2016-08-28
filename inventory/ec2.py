#!/usr/bin/env python

from boto import ec2
import json

inventory = {}
inventory['_meta'] = { 'hostvars': {} }
inventory['all'] = []


#
# Make boto connection
#

# FIXME: Error check
ec2conn = ec2.connection.EC2Connection()
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
    krole = None
    try:
      krole = "tag_krole_" + i.tags['krole']
    except: 
      pass

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
