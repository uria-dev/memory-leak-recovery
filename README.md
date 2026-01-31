# memory-leak-recovery
An app that introduces an API, intentionally creates a memory leak, and recovers from it. 

## How does it work?
The app is a simplem python script that creates a FastAPI endpoint on port 8000. Just GET the `/leak` endpoint, and it will start the memory leak.

## k8s deployment
The idea of this app is to showcase theself-healing abilities of Kubernetes. Once you have this running locally (I used minikube), use the following command to port-forward this:

`kubectl port-forward memory-leak-recovery-6f4fdf64fb-gmsn9 8000:8000`

Naturally, your own pod will have a different hash and PID to my own. 

Once the server is running, you can use something like `kubectl get pods -w` (in a sepoarate terminal window) to keep an eye on the pods. Then, you can just curl `localhost:8000` or navigate to it with the brower. You'll eventually see the pod get OOMKilled and then restarted!