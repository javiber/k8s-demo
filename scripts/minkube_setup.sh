#!/usr/bin/env bash
set -e


print_usage() {
  printf "confugure minikube\n"
  printf "Usage:\n"
  printf "  minikube_setup [-g]\n"
  printf "Options:\n"
  printf "  -g: setup minikube with gpu support\n"
}

gpu='false'
while getopts ':hg' flag; do
  case "${flag}" in
    g) gpu='true' ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [[ "${gpu}" == "true" ]]; then
    printf "Configuring minikube with GPU, following https://minikube.sigs.k8s.io/docs/tutorials/nvidia_gpu/#using-the-none-driver\n"
    # driver none needs sudo but starting with sudo creates some issues
    # first something related to systemd
    # https://github.com/kubernetes/minikube/issues/7053
    sudo sysctl fs.protected_regular=0
    sudo minikube start --driver=none --apiserver-ips 127.0.0.1 --apiserver-name localhost
    # if minikube finished without errors everything is good except that kubctl is configured for root
    # the rest of this fixes the issues
    rm -rf ~/.minikube
    rm -rf ~/.kube
    sudo mv /root/.minikube /home/$USER/.minikube
    sudo mv /root/.kube /home/$USER/.kube
    sudo chown -R $USER $HOME/.minikube
    sudo chown -R $USER $HOME/.kube
    sed -i "s#root#home/$USER#g" ~/.kube/config

    # install recommended plugin
    kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/master/nvidia-device-plugin.yml
    # check that GPU is available on the node
    kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
else
    printf "Configuring minikube normally\n"
    minikube start --kubernetes-version=1.21.7
fi

minikube addons enable dashboard
minikube addons enable metrics-server
minikube status
minikube addons list