# Smoke Test

This lab walks you through a quick smoke test to make sure things are working.

```
$ ansible-playbook 09-smoketest.yml
```

Please note that this set of playbooks does not currently configure Kubernetes to automatically create AWS loadbalancers and thus there is no loadbalancer to access the nginx pod.

Once this playbook is run you can login to one of the controllers, get the port nginx is running on, and curl that port on one of the workers.

```
ubuntu@controller0:~$ kubectl get svc nginx --output=jsonpath='{range .spec.ports[0]}{.nodePort}'
30219
ubuntu@controller0:~$ curl worker0:30219
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
