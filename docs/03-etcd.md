# Bootstrapping a H/A etcd cluster

In this lab you will bootstrap a 3 node etcd cluster.

## Why

All Kubernetes components are stateless which greatly simplifies managing a Kubernetes cluster. All state is stored
in etcd, which is a database and must be treated special. etcd is being run on a dedicated set of machines for the 
following reasons:

* The etcd lifecycle is not tied to Kubernetes. We should be able to upgrade etcd independently of Kubernetes.
* Scaling out etcd is different than scaling out the Kubernetes Control Plane.
* Prevent other applications from taking up resources (CPU, Memory, I/O) required by etcd.

## Provision the etcd Cluster

```
$ ansible-playbook 03-etcd.yml
```
