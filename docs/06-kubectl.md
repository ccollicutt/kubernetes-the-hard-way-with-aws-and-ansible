# Configuring the Kubernetes Client - Remote Access

This lab will configure the utility (util0) server as a kubectl client machine.

```
$ ansible-playbook 06-kubectl.yml
```

Then you can ssh into the util node and run kubectl commands.

```
$ ssh -F ssh_config util0
```

Now you should be able to connect securely to the remote API server:

```
ubuntu@util0:~$ kubectl get componentstatuses
NAME                 STATUS    MESSAGE              ERROR
scheduler            Healthy   ok                   
controller-manager   Healthy   ok                   
etcd-0               Healthy   {"health": "true"}   
etcd-1               Healthy   {"health": "true"}   
etcd-2               Healthy   {"health": "true"}   
```

```
ubuntu@util0:~$ kubectl get nodes
NAME      STATUS    AGE
worker0   Ready     4h
worker1   Ready     4h
worker2   Ready     4h
```
