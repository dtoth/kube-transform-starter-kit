# kube-transform-starter-kit

This starter kit provides reusable infrastructure and build resources for quickly deploying [`kube-transform`](https://github.com/dtoth/kube-transform) pipelines.

> This kit is optional — see the kube-transform repo for minimum setup requirements if you'd rather build your own stack from scratch.

## What’s Included

- ✅ Local (Minikube) and Remote (Autoscaling EKS) deployment setups
  - Docker build scripts & base images
  - Terraform configs for AWS
  - RBAC and service account templates
- ✅ Example projects (see `examples/` folder)

---

## Getting Started

### 1. Run Hello World Locally

Try `kube-transform` with a local Kubernetes cluster using Minikube.

- Set up your local cluster:\
  See [`docs/run_local_k8s.md`](docs/run_local_k8s.md)

- Run the Hello World pipeline:\
  Open and run the notebook at [`examples/hello_world/run.ipynb`](examples/hello_world/run.ipynb)

### 2. Scale Up to EKS

Once local is working, switch to a remote autoscaling AWS cluster with no code changes:

- Set up AWS resources:\
  See [`docs/run_eks_k8s.md`](docs/run_eks_k8s.md)

- Update your `kt-contexts.json` with the new `image_path`, `data_dir`, and `kube_context`

- Re-run the Hello World pipeline with `CONTEXT = 'eks'`

---

## Examples

This repo contains example projects that demonstrate how to structure and deploy real `kube-transform` pipelines:

- [`examples/hello_world`](examples/hello_world) — a minimal first pipeline
- More coming soon...

Each example includes:

- Source code and pipeline spec
- Notebook to run the pipeline

See each folder’s `README.md` for details.

---

## Writing Your Own Pipelines

To build your own pipeline:

- Start by copying the structure of an existing example project
- Use your own functions under `kt_functions/`
- Modify the pipeline spec to match your task flow

More guidance on writing custom pipelines coming soon!

