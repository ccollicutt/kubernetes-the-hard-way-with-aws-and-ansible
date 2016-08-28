# Setting up a Certificate Authority and TLS Cert Generation

In this lab you will setup the necessary PKI infrastructure to secure the Kubernetes components. This lab will leverage CloudFlare's PKI toolkit, [cfssl](https://github.com/cloudflare/cfssl), to bootstrap a Certificate Authority and generate TLS certificates.

In this lab you will generate a single set of TLS certificates that can be used to secure the following Kubernetes components:

* etcd
* Kubernetes API Server
* Kubernetes Kubelet

> In production you should strongly consider generating individual TLS certificates for each component.

After completing this lab you should have the following TLS keys and certificates in the ./fetched directory and those certificates will be placed where necessary in the various instances.

```
ca-key.pem
ca.pem
kubernetes-key.pem
kubernetes.pem
```

## Setup Certificate Authority and generate certificates

```
$ ansible-playbook 02-certificate-authority.yml
```

