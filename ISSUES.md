# Issues

* When running all the playbooks serially without much time in between the deployment will often fail--perhaps etcd takes a while to come up, even though it's reporting as healthy?
* When using "--cloud-provider=aws" kube-controller-manager will look for a route with a specific tag, need to get this working
