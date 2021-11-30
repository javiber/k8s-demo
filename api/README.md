# API demo
Simple demo of how to deploy a basic API on kubernetes. The demo has 3 stages from simpler to more complex deployment strategies.

## Setup

1. Start vanilla minikube with `bash scripts/minkube_setup.sh`
1. Point docker-cli to minikube's docker-server `eval $(minikube docker-env)`
1. Build api with `docker build -t api:v0.1.0` inside `api/` folder

## deploy basic API
1. create services with `kubectl apply -f deploy/api/networking.yml`
1. create deployment with `kubectl apply -f deploy/api/deployment.yml`
1. test that the api works with `minikube service api-svc-stable`

## istio
1. setup [istio](https://istio.io/latest/docs/setup/getting-started/#download)
1. deploy istio components with `kubectl apply -f deploy/api/istio.yml`
1. open another terminal and run `minikube tunnel`
1. get ingress IP with `INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')`
1. run the consumer with `python api/consumer.py -e http://$INGRESS_HOST`

## Argo rollouts
1. cleanup with `kubectl delete deployment api`
1. install argo rollouts and it's kubectl addon
1. add [prometheus for istio](https://istio.io/latest/docs/ops/integrations/prometheus/)
1. add rollout `kubectl apply -f deploy/api/rollout.yml` first time is going to ignore canary and deploy inmediatelly
1. modify `api/app.py` and the version in `app/__init__.py`
1. build new version with `docker build -t api:v0.1.1` inside `api/` folder
1. deploy new version with `kubectl argo rollouts set image api-rollout api=api:<NEW_VERSION>`
1. watch progress with  `kubectl argo rollouts get rollout api-rollout --watch`

You can run 2 consumers while rolling the deployment, and set the user to `juancarlo` on one of them. There is a special rule on the [virtual service](../deploy/api/networking.yml) that always routes this user to the stable version.


Troubleshoot:
- Wierd 503 certificate errors: `kubectl delete -n istio-system pod istio-ingressgateway-<Tab>`