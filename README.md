# k8s-demo

## local setup

1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
1. run `bash scripts/minkube_setup.sh [-g]`

## run a training job

1. Fix hostPath in `deploy/train/setup.yml` if necessary
1. `kubectl apply -f deploy/train/setup.yml` to config namespace and volumes
1. `kubectl apply -f deploy/train/job.yml` to submit the job
1. `kubectl get po --namespace=train` to check the status and the name of the pod
1. `kubectl logs <pod-name> --namespace=train`

To avoid passing the namespace on each command you can use `config set-context --current --namespace=train`