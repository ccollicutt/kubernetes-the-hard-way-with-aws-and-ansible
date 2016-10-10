Please note that this repository is frozen, but work is continuing in [sk8ts](https://github.com/sk8ts).

# Kubernetes the Hard Way in AWS with Ansible

This implements [Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way) (KtHW) but with two major differences: 1) it uses Ansible and 2) it's deployed on AWS instead of Google Compute Engine. Basically it mimics the manual steps of KtHW in simple Ansible playbooks. No roles are used, as it is more of a serial procedure in terms of being an example of installing Kubernetes. This is really for learning about AWS and Kubernetes, not for creating any kind of production system. :)

As a thank you, I want to note that I  would have had difficulty doing this in AWS without [Kubernetes the hard way AWS](https://github.com/ivx/kubernetes-the-hard-way-aws), which takes KtHW and modifies it to use the AWS CLI.

There are several "edge cases" I ran into during the development of this series of playbooks, especially around using AWS and Ansible. Over time I hope to clear out these edge cases. Even in something simple like this set of playbooks there is much to be improved.

## Infrastructure Expectations

1. You are using AWS
1. You have AWS permissions and credentials to create at least ten virtual machines (yup ten)
1. Your AWS credentials are exported as environment variables in your current shell session. See the vars/all.yml file.
1. Nodes are Ubuntu 16.04/Xenial, ie. are created from a Xenial AMI.

## Ansible Expectations

1. You have ansible 2.1 or higher, probably running from a Python virtual environment.
1. You have the library requirements listed in requirements.txt.
1. You are going to run Ansible from your local computer. With some simple modification you could run this from anywhere, including inside AWS which would be faster if you would like.

## Deploy Kubernetes

NOTE: This uses spot instances by default.

* [Cloud Infrastructure Provisioning](docs/01-infrastructure.md)
* [Setting up a CA and TLS Cert Generation](docs/02-certificate-authority.md)
* [Bootstrapping an H/A etcd cluster](docs/03-etcd.md)
* [Bootstrapping an H/A Kubernetes Control Plane](docs/04-kubernetes-controller.md)
* [Bootstrapping Kubernetes Workers](docs/05-kubernetes-worker.md)
* [Configuring the Kubernetes Client - Remote Access](docs/06-kubectl.md)
* [Managing the Container Network Routes](docs/07-network.md)
* [Deploying the Cluster DNS Add-on](docs/08-dns-addon.md)
* [Smoke Test](docs/09-smoke-test.md)
* [Cleaning Up](docs/10-cleanup.md)

## Inventory File

There is a custom inventory file that comes with this repository. It will only report nodes with a "krole" tag. Other nodes will not be reported by the custom Ansible inventory.

## Ansible and SSH

Ansible performs its work over SSH. That means each server Ansible needs to configure must be accessible over SSH. To do that this set of playbooks will provision an AWS VPC with a public and private network, and a utility (util0) node will be provisioned in the public subnet and be provided a public IP address. A security group will be setup to allow SSH to that instance. Ansible will use that util0 server as a jump host to access the other instances, which have been created in the private subnet. While the instances in the private subnet can access the internet through a NAT gateway, they are not directly accessible from the Internet.

Once the instances have been provisioned there is a playbook to create a local ssh_config file that Ansible will use to access all AWS EC2 instances.

## Future Work

* DONE: use_spots variable to turn on/off using spot instances
* DONE: Move ensuring python2 into user-data?
* Create an ssh key for use with AWS
* Some interesting work done [here](https://github.com/opencredo/k8s-terraform-ansible-sample)
* Create k8 "deployments" using an Ansible module instead of running from shell commands (eg. the nginx smoketest)
* Use roles
* Better DNS integration
* Deletion playbook to remove everything
* Better understanding of availability zones

### (Better) AWS Integration

Currently this repository will setup Kubernetes so that it can add pod routes to the VPC route table and setup elastic load balancers. There are other AWS integrations that still need to be completed. But in general the Kubernetes deployed by this repository will be useful because it will automatically setup EC2 load balancers.

* DONE: K8s to create loadbalancers for deployments
* DONE: Pod routes being automatically added
* Autoscaling
* Stateful block storage with EBS

Most of what Kubernetes does in AWS is [documented](https://github.com/kubernetes/kubernetes/blob/master/docs/design/aws_under_the_hood.md).

### Security

* Not running things as root
* Verify all binary downloads
