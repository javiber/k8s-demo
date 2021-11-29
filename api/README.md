Setup

1. setup minikube without gpu
1. setup [istio](https://istio.io/latest/docs/setup/getting-started/#download)
1. build api with `python scripts/build_api.py`
1. deploy api with `kubectl apply -f deploy/api/deployment.yml`
1. test that the api works with `minikube service api`
1. deploy istio components with `kubectl apply -f deploy/api/istio.yml`
1. open another terminal and run `minikube tunnel`
1. get ingress IP with ` INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')`
1. run the consumer with `python api/consumer.py -e http://$INGRESS_HOST`

Troubleshoot:
- Wierd 503 certificate errors: `kubectl delete -n istio-system pod istio-ingressgateway-<Tab>`