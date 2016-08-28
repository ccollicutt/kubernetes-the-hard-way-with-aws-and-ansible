# Managing the Container Network Routes

Now that each worker node is online we need to add routes to make sure that Pods running on different machines can talk to each other. In this lab we are not going to provision any overlay networks and instead rely on Layer 3 networking. That means we need to add routes to our AWS VPC. 

In AWS networks and subnets can have route tables, which is what this playbook configures, pointing the pod CIDRs to specific instances.

```
$ ansible-playbook 07-pod-routes.yml
```

