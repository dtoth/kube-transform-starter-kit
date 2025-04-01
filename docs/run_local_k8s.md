This guide will walk you through running a local kubernetes cluster via Minikube.

Pre-requisites:
- You're running Mac OSX (this has been tested with Sonoma 14.5)
- You've installed homebrew

Run these commands from the root `kube_transform_starter_kit` directory.

### Install Docker Desktop and run it
```
brew install --cask docker
open /Applications/Docker.app
```
Within Docker Desktop, go to Settings/Resources, ensure you have at least 8.5 GB allocated, and then restart Docker Desktop.

### Install minikube and kubectl
```
brew install minikube
minikube config set driver docker
brew install kubectl
```

### Run a local minikube k8s cluster
The commands below run a local k8s cluser with Minikube. The cluster mounts your local data folder to /mnt/data. This folder will be used as the shared file store across all pods.

```
minikube start --cpus=4 --memory=8192mb --mount --mount-string=$(pwd)/data/:/mnt/data --extra-config=kubelet.system-reserved="memory=512Mi"
minikube addons enable metrics-server
minikube dashboard
```

Now you should see a browser window open with a Minikube dashboard.

### Create the kt-pod service account
```
kubectl apply -f resources/kubernetes/kt-pod-rbac.yaml
```

This creates a Kubernetes service account called `kt-pod`, and says that pods holding this service account can create Jobs in the default namespace in your cluster.

`kube-transform` assigns this service account to its controller pods, so it must exist in your cluster.

Congrats! Your cluster is ready to use.


### Helpful Tips

#### List pods/jobs and resource usage 
```
kubectl top pods
kubectl get pods
kubectl get jobs
```

#### Get pod logs
`kubectl logs <pod_name>`


#### Shut down minikube (e.g. if you need to restart the cluster)
```
minikube stop
minikube delete
```