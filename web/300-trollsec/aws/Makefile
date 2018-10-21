# bsidespdx2018 is the organization on dockerhub
REGISTRY := bsidespdx2018
DOCKER_IMAGE := web300

CONTAINER_TAG := ${REGISTRY}/${DOCKER_IMAGE}

target: container push deploy serve

# Docker Configurations

container:
	docker build --no-cache --tag ${CONTAINER_TAG} ../src

push: 
	docker push ${CONTAINER_TAG}

# Kubernetes

deploy:
	cat deployment/deploy.yaml | kubectl create --namespace bsidespdxctf  -f -

serve:
	kubectl create --namespace bsidespdxctf -f deployment/service.yaml

deleteKube:
	cat deployment/deploy.yaml | kubectl delete --namespace bsidespdxctf -f -
	kubectl delete --namespace  bsidespdxctf -f deployment/service.yaml
