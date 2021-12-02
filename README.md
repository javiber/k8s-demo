# k8s-demo

Example of a couple of use cases for kubernetes that could be useful in ML.

## Demos

1. First demo shows how to train a pytorch model for MNIST as a Kubernetes Job. See [train](./train) for more details
1. Second demo shows how to use canary deployments on a simple API. See [api](./api) for more details

## Local setup

1. Install [docker](https://docs.docker.com/get-docker/)
1. Clone this repo
1. Optionally but recommended:
    1. Install [pyenv](https://github.com/pyenv/pyenv#installation) and run `pyenv install`
    1. Setup a virtualenv with `python -m venv .venv` and activate with `source .venv/bin/activate`
    1. Install dev requirements with `pip install -r requirements.txt`
1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/)


## Cluster setup
I only tested this on minikube, for the first demo I used my local GPU on minikube which requires sudo for alternatives look into [train](./train).

### Minikube setup
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
1. Use [this script](./scripts/minikube_setup.sh) to setup a GPU-enabled cluster or a vanilla cluster.
