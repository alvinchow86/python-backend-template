TAG = latest
DOCKER_LOCAL = alvinchow-service:$(TAG)
DOCKER_REPO = something.dkr.ecr.us-west-2.amazonaws.com/alvinchow-service
DOCKER_REMOTE = $(DOCKER_REPO):$(TAG)

.PHONY: build
build:
	docker build -t $(DOCKER_LOCAL) --build-arg FURY_AUTH .

push:
	docker tag $(DOCKER_LOCAL) $(DOCKER_REMOTE)
	docker push $(DOCKER_REMOTE)

buildpush: build push
