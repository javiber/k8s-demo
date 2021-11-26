docker build -t train:v1 .
docker run --gpus=all --shm-size 8G -it -e CACHE_PATH=/.cache -v $PWD:/code -v $PWD/.cache:/.cache train:v1 bash