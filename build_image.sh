#!/bin/bash -e
docker_user=$DOCKER_USER
image_tag=$IMAGE_TAG
app_name=pieces-demo
image_name=${docker_user}/${app_name}
full_image_name=${image_name}:${image_tag}
cd "$(dirname "$0")" 
pwd
docker build -t "${full_image_name}" -f Dockerfile .
docker push "$full_image_name"

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"