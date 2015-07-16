PROJECT ?= imio/eid
TAG     ?= latest
IMAGE=$(PROJECT):$(TAG)
clean:
	docker-compose rm --force
build:
	export USERID=$(shell id -u -r) && \
	cat Dockerfile.tmpl | envsubst > Dockerfile
	docker build -t $(IMAGE) .
	docker run --name belgianeidauthplugin $(IMAGE) bash
	docker cp belgianeidauthplugin:/code/devel .
	docker cp belgianeidauthplugin:/code/var .
	docker rm belgianeidauthplugin
	rm Dockerfile
up:
	docker-compose run --service-ports web
run: up
test:
	docker-compose run web /code/bin/test
debug-instance:
	docker-compose run web /code/bin/instance debug
debug:
	docker run -p 8080:8080 -v $(PWD)/Products:/code/Products -ti $(IMAGE) /bin/bash
dev:
	docker-compose run webdev
