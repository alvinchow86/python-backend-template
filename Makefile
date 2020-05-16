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

buildproto:
	alvinchow_service/api/grpc/makeprotobufs

proto: buildproto
	mkdir -p dist && \
	cp -r alvinchow_service/api/grpc/dist/*.tar.gz dist
