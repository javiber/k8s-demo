# k8s-demo

## local setup

1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
1. Install [pyenv](https://github.com/pyenv/pyenv#installation) and run `pyenv install`
1. setup a virtualenv with `python -m venv .venv` and activate with `source .venv/bin/activate`
1. install dev requirements with `pip install -r requirements.txt`

## Demos

1. First demo shows how to train a pytorch model for MNIST as a Kubernetes Job. See [train](./train) for more details
1. Second demo shows how to use canary deployments on a simple API. See [api](./api) for more details


## GKE
Only tested moving train to GKE, these are steps/changes  comparing it to minikube needed

1. Setup a cluster
    1. Create a cluster following https://cloud.google.com/kubernetes-engine/docs/how-to/gpus. In my case I tested with:
        - Asked to increase quota on GCP to 1 K80
        - GKE Standard because autopilot doesn't support GPU
        - regional cluster in `us-east1-c`
        - one node pool with 1 node (autoescaling from 0-3) of type `e2-medium` (I think they could be even smaller)
        - one node pool with 0 node (autoescaling from 0-1) of type `n1-standard-2` with 1 `NVIDIA Tesla K80`
        - enabled Node auto-provisioning
    1. Config kubectl with `gcloud container clusters get-credentials <CLUSTER_NAME> --region <REGION> --project <GCP_PROJECT>`
    1. Config GCR with `gcloud auth configure-docker gcr.io`
1. Pushing images changes
    1. Build images using tag `gcr.io/<GCP_PROJECT>/<REPO_NAME>/train:v1`
    1. Push images to GCR with `docker push` (have a coffee in the meantime)
1. Use `deploy/train/gke_*` yamls updating the images to match the tags we used above
