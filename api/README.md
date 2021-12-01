# API demo
Simple demo of how to deploy a basic API on kubernetes. The demo has 3 stages from simpler to more complex deployment strategies.

## Setup
Basic setup of minikube and docker

1. Start vanilla minikube with `bash scripts/minkube_setup.sh`
1. Point docker-cli to minikube's docker-server `eval $(minikube docker-env)`
1. Build api with `docker build -t api:v0.1.0` inside `api/` folder

## Deploy basic API
Deploy app using vanilla kubernetes

1. Create services with `kubectl apply -f deploy/api/networking.yml`
1. Create deployment with `kubectl apply -f deploy/api/deployment.yml`
1. Test that the api works with `minikube service api-svc-stable`

## Istio
Introduce Istio for smarter rounting

1. Setup [istio](https://istio.io/latest/docs/setup/getting-started/#download)
1. Create istio's components with `kubectl apply -f deploy/api/istio.yml`
1. Open another terminal and run `minikube tunnel`
1. Get ingress IP with `INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')`
1. Run the consumer with `python api/consumer.py -e http://$INGRESS_HOST`

## Argo rollouts
Introduce Argo rollouts for Canary deployments

1. Cleanup with `kubectl delete deployment api`
1. Install [argo rollouts](https://argoproj.github.io/argo-rollouts/installation/) and it's kubectl addon
1. Install [prometheus for istio](https://istio.io/latest/docs/ops/integrations/prometheus/)
1. Create rollout `kubectl apply -f deploy/api/rollout.yml` first time is going to ignore canary and deploy inmediatelly
1. Modify `api/app.py`
1. Build new version with `docker build -t api:v0.1.1` inside `api/` folder
1. Deploy new version with `kubectl argo rollouts set image api-rollout api=api:<NEW_VERSION>`
1. Watch progress with  `kubectl argo rollouts get rollout api-rollout --watch`

You can run 2 consumers while rolling the deployment, and set the user to `juancarlo` on one of them. There is a special rule on the [virtual service](../deploy/api/networking.yml) that always routes this user to the stable version.


Troubleshoot:
- Wierd 503 certificate errors: `kubectl delete -n istio-system pod istio-ingressgateway-<Tab>`