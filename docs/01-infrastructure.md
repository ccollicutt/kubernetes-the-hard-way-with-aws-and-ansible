# Cloud Infrastructure Provisioning

Kubernetes can be installed just about anywhere physical or virtual machines can be run. In this lab we are going to focus on Amazon Web Services (IaaS).

This lab will walk you through provisioning the compute instances required for running a H/A Kubernetes cluster. A total of 10 virtual machines will be created, one of which is a utility/jump host.

After completing this guide you should have the following compute instances, as shown by using the custom Ansible inventory file which reports JSON. 

````
$ ./inventory/ec2.py 
{
    "all": [
        "controller2", 
        "worker1", 
        "controller1", 
        "worker2", 
        "util0", 
        "etcd0", 
        "worker0", 
        "etcd1", 
        "etcd2", 
        "controller0"
    ], 
    "_meta": {
        "hostvars": {
            "etcd2": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "etcd1": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "etcd0": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "worker1": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "util0": {
                "ansible_ssh_host": "YYY.YYY.YYY.YYY"
            }, 
            "worker2": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "controller2": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "controller1": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "controller0": {
                "ansible_ssh_host": "172.20.1.XXX"
            }, 
            "worker0": {
                "ansible_ssh_host": "172.20.1.XXX"
            }
        }
    }, 
    "tag_krole_worker": [
        "worker1", 
        "worker2", 
        "worker0"
    ], 
    "tag_krole_util": [
        "util0"
    ], 
    "tag_krole_etcd": [
        "etcd0", 
        "etcd1", 
        "etcd2"
    ], 
    "tag_krole_controller": [
        "controller2", 
        "controller1", 
        "controller0"
    ]
}

````

> All machines will be provisioned with *dynamic* IP addresses

To make our Kubernetes control plane remotely accessible, a public IP address will be provisioned and assigned to a Load Balancer that will sit in front of the 3 Kubernetes controllers.

## First Setup Variables

Before we run all the playbooks we need to setup a couple of variables.

```
$ cp vars/all.yml.example vars/all.yml
$ vi vars/all.yml
```

1. Set the right *ec2_key_name* variable.
1. Ensure the variable *image* is the right one for the region you are using. These playbooks expect Ubuntu 16.04/Xenial and probably nodes with local disk.
1. Please note the *aws_* key and region variables which are using environment lookups. Ensure that those enviroment variables are set in your current shell session, or perhaps enter those keys directly into the all.yml file.
1. Set the *vpc_subnet_az* to the right availability zone

## Create IAM Roles and Policies

Because Kubernetes can add AWS load balancers, setup route tables, add security groups, and otherwise alter AWS, we need to provide it with permissions to do that.

```
$ ansible-playbook 00-iam.yml
```

This will create a master and worker role/policy. Instances will be assigned one of the two roles.

## Create a Custom Network

We need some custom networking. This creates a new VPC with a public and private subnet, as well as and internet and NAT gateways.

```
$ ansible-playbook 00-vpc.yml
```

### Create Instances

Please note that by default *spot instances* will be used, which you would probably not want to do in production. But for testing they can be 80% cheaper.

If you don't want to use spot instances, set *use_spots* to false in *vars/all.yml*.


```
$ ansible-playbook 01-infrastructure.yml
```

### Ensure instances are in the local ssh_config file

Once the instances are created Ansible needs to be able to ssh into them, and that is probably best done by setting up a local ssh_config file.

The below playbook will create that file so the rest of the playbooks can use it.

```
$ ansible-playbook 01-localhost-ssh-config.yml
```

Once this playbook completes there will be a *./ssh_config file.

## ZFS

Please note the user-data file for the worker nodes installs and configures ZFS for use with Docker. This may not be what you want.
