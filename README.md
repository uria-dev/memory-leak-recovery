# memory-leak-recovery

An app that intentionally creates a memory leak to demonstrate Kubernetes self-healing and autoscaling. It exposes a FastAPI server on port 8000 - hit the `/leak` endpoint and watch as the HPA scales up pods, the leaking pod gets OOMKilled, and the app stays available throughout.

## Prerequisites

Make sure you have the following installed:

- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Docker](https://docs.docker.com/get-docker/)

## Setup

### 1. Start minikube

```bash
minikube start
```

### 2. Build the Docker image

Point your shell to minikube's Docker daemon so the image is available to the cluster without pushing to a registry:

```bash
eval $(minikube docker-env)
docker build -t memory-leak-recovery:1.0.0 .
```

### 3. Deploy the app

```bash
helm install memory-leak-recovery ./helm
```

> The ServiceMonitor will fail to apply at this point because the Prometheus CRDs don't exist yet. That's expected - we'll fix it in step 5.

### 4. Install the monitoring stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

### 5. Upgrade the app

Now that the Prometheus CRDs are installed, upgrade the release so the ServiceMonitor gets created:

```bash
helm upgrade memory-leak-recovery ./helm
```

### 6. Access the app

In a terminal, port-forward to the service:

```bash
kubectl port-forward svc/memory-leak-recovery 8000:8000
```

Then open http://localhost:8000 in your browser (or `curl localhost:8000`).

### 7. Access Grafana

Get the admin password:

```bash
kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d
```

Port-forward to Grafana:

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Open http://localhost:3000 and sign in with username `admin` and the password from above.

## Trigger the leak and observe

1. Open a second terminal and watch pods:

   ```bash
   kubectl get pods -w
   ```

2. Trigger the memory leak:

   ```bash
   curl localhost:8000/leak
   ```

   This starts appending ~10 MB/s to an in-memory list. As memory usage climbs:

   - The **HPA** detects memory utilization crossing 40% and scales up new pods.
   - The leaking pod eventually hits its 1024 Mi memory limit and gets **OOMKilled**.
   - The app **stays available** throughout - you can still `curl localhost:8000` because the other pods are healthy.
   - After the leaking pod restarts and memory drops, the extra pods scale back down after ~5 minutes.

## Grafana dashboard setup

1. In Grafana, go to **Dashboards** > **New** > **New Dashboard** > **Add visualization**.
2. Select the **Prometheus** data source.
3. Choose the **Time Series** visualization type.
4. In the metrics browser, use the metric: `memory_total_percentage`
5. Under **Options** > **Legend**, set it to `{{pod}}` so each pod gets its own line.
6. Click **Apply** and watch the memory usage climb in real time after triggering the leak.
