SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DOCKERFILE_PATH=$SCRIPT_DIR/../docker/Dockerfile

# Build the docker image and register it with minikube
eval $(minikube docker-env)
docker build -t kt-image:latest -f $DOCKERFILE_PATH .