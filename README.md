# memory-leak-recovery
An app that introduces an API, intentionally creates a memory leak, and recovers from it. 

## How does it work?
The app is a simplem python script that creates a FastAPI endpoint on port 8000. Just curl the `/leak` endpoint, and it will start the memory leak.

## k8s deployment
The idea of this app is to showcase the self-healing abilities of Kubernetes. Once you have this running locally (I used minikube), use the following command to port-forward this:

`kubectl port-forward memory-leak-recovery-6f4fdf64fb-gmsn9 8000:8000`

Naturally, your own pod will have a different hash and PID to my own. 

Once the server is running, you can use something like `kubectl get pods -w` (in a sepoarate terminal window) to keep an eye on the pods. Then, you can just curl `localhost:8000` or navigate to it with the brower. 

### What you can see

Once you have everything set up correctly and you curl the /leak endpoint, you should be able to see more pods spin up as the pod uses more and more memory. Eventually, the pod will OOMKill, but because there are other pods the application never goes down - you can still curl `localhost:8000` without any problem, even after the other pod is OOMKilled.
Due to how k8s scaling works, the pods will stay up for around 5 minutes after the leaking pod is restarted, after which they'll all just quietly terminate.
