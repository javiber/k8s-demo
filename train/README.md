
## testing on docker:
1. docker build -t train:dev .
1. docker run --gpus=all --shm-size 8G -it -e CACHE_PATH=/.cache -v $PWD:/code -v $PWD/.cache:/.cache train:dev python train.py