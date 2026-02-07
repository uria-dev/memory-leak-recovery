# memory-leak-recovery
An app that introduces an API, intentionally creates a memory leak, and recovers from it. 

## How does it work?
The app is a simple python script that creates a FastAPI endpoint on port 8000. Just curl the `/leak` endpoint, and it will start the memory leak.

## How to set it up

Start with installing the monitoring stack, `helm install monitoring prometheus-community/kube-prometheus-stack ...`
Then make sure to build and deploy the app, using `docker build` and `helm install`

## k8s deployment
The idea of this app is to showcase the self-healing abilities of Kubernetes. Once you have this running locally (I used minikube), use the following command to port-forward this:

`kubectl port-forward svc/memory-leak-recovery 8000:8000`

Once the server is running, you can use something like `kubectl get pods -w` (in a separate terminal window) to keep an eye on the pods. Then, you can just curl `localhost:8000` or navigate to it with the browser. 

## What you can see

Once you have everything set up correctly and you curl the /leak endpoint, you should be able to see more pods spin up as the pod uses more and more memory. Eventually, the pod will OOMKill, but because there are other pods the application never goes down - you can still curl `localhost:8000` without any problem, even after the other pod is OOMKilled.
Due to how k8s scaling works, the pods will stay up for around 5 minutes after the leaking pod is restarted, after which they'll all just quietly terminate.

## Grafana dashboard

I've also added a Grafana dashboard into this. You can spin it up with `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80`. Once that's set up, you can go to `localhost:3000` and you can sign in with the `admin` username and the password that you get from this command:
`kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d`