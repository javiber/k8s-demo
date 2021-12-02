# Train a model demo
On this demo we'll train a pytorch model as a kubernetes job using GPU.

## run a training job using your local GPU

1. start minikube with GPU `bash scripts/minkube_setup.sh -g` (needs sudo)
1. Create a folder to store the cache and use it as the hostPath in `deploy/train/setup.yml`
1. `kubectl --namespace=train apply -f deploy/train/setup.yml` to config namespace and volumes
1. `kubectl --namespace=train apply -f deploy/train/job.yml` to submit the job
1. `kubectl --namespace=train get pod` to check the status and the name of the pod
1. `kubectl --namespace=train logs <pod-name>`

To avoid passing the namespace on each command you can use `kubectl config set-context --current --namespace=train`

## GKE
If you want to run this demo on GKE, here is a loose summary of the changes you need

1. Seting up a cluster, You will need to enable billing. I made all my tests and was able to run 1 job in a few hours for ~ u$d 0.5
    1. Create a cluster following this [guide](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus). In my case I used:
        - Asked to increase all-regions quota on GCP to 1 K80.
        - GKE Standard because autopilot doesn't support GPU
        - regional cluster in `us-east1-c` (K80s are available there)
        - one node pool with 1 node (autoescaling from 0-3) of type `e2-medium` (I think they could be even smaller)
        - one node pool with 0 node (autoescaling from 0-1) of type `n1-standard-2` with 1 `NVIDIA Tesla K80`
        - enabled Node auto-provisioning
    1. Config kubectl with `gcloud container clusters get-credentials <CLUSTER_NAME> --region <REGION> --project <GCP_PROJECT>`
    1. Config GCR with `gcloud auth configure-docker gcr.io`
1. Pushing images changes. [Docs](https://cloud.google.com/container-registry/docs/pushing-and-pulling)
    1. Enable this API in GCP
    1. Build images using tags `gcr.io/<GCP_PROJECT>/<REPO_NAME>/train:v1`
    1. Push images to GCR with `docker push` (have a coffee in the meantime)
1. Use `deploy/train/gke_*` yamls updating the images to match the tags we used above


## testing on vanilla docker before deploying:
1. docker build -t train:dev .
1. docker run --gpus=all --shm-size 8G -it -e CACHE_PATH=/.cache -v $PWD:/code -v $PWD/.cache:/.cache train:dev python train.py