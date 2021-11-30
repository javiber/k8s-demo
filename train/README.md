## run a training job

1. start minikube with GPU `bash scripts/minkube_setup.sh -g`
1. Fix hostPath in `deploy/train/setup.yml` if necessary
1. `kubectl --namespace=train apply -f deploy/train/setup.yml` to config namespace and volumes
1. `kubectl --namespace=train apply -f deploy/train/job.yml` to submit the job
1. `kubectl --namespace=train get pod` to check the status and the name of the pod
1. `kubectl --namespace=train logs <pod-name>`

To avoid passing the namespace on each command you can use `kubectl config set-context --current --namespace=train`

## testing on docker:
1. docker build -t train:dev .
1. docker run --gpus=all --shm-size 8G -it -e CACHE_PATH=/.cache -v $PWD:/code -v $PWD/.cache:/.cache train:dev python train.py