SHELL := /usr/local/bin/bash

HUB_NAMESPACE  = "mamercad"
IMAGE_NAME     = "hello"
IMAGE_TAG      = "blue"
DEPLOY_NAME    = "deployment/hello"
LISTEN_OUTSIDE = 5000
LISTEN_INSIDE  = 5000

.PHONY: build
build:
	docker build --build-arg tag=$(IMAGE_TAG) -t $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: run
run: build
	docker run -d --rm -p $(LISTEN_OUTSIDE):$(LISTEN_INSIDE) --env tag=$(IMAGE_TAG) $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: push
push: build
	docker push $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: blue
blue:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):blue --record=true

.PHONY: green
green:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):green --record=true

.PHONY: flipflop
flipflop:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):blue --record=true
	sleep 60
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):green --record=true
	sleep 60
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):blue --record=true
	sleep 60
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):green --record=true
	sleep 60
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):blue --record=true
	sleep 60
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):green --record=true

.PHONY: server
server:
	kubectl apply -f $(IMAGE_NAME).yaml

.PHONY: client
client:
	source venv/bin/activate && ./client.py
