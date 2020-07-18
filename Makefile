SHELL := /usr/local/bin/bash

HUB_NAMESPACE  = "mamercad"
IMAGE_NAME     = "hello"
IMAGE_TAG_V1   = "blue"
IMAGE_TAG_V2   = "green"
DEPLOY_NAME    = "deployment/hello"
LISTEN_OUTSIDE = 5000
LISTEN_INSIDE  = 5000

.PHONY: build-blue
build-blue:
	docker build --build-arg tag=$(IMAGE_TAG) -t $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1) .

.PHONY: build-green
build-green:
	docker build --build-arg tag=$(IMAGE_TAG) -t $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2) .

.PHONY: run-blue
run-blue: build-blue
	docker run -d --rm -p $(LISTEN_OUTSIDE):$(LISTEN_INSIDE) --env tag=$(IMAGE_TAG) $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1)

.PHONY: run-green
run-green: build-green
	docker run -d --rm -p $(LISTEN_OUTSIDE):$(LISTEN_INSIDE) --env tag=$(IMAGE_TAG) $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2)

.PHONY: push
push: build-blue build-green
	docker push $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1)
	docker push $(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2)

.PHONY: flip-blue
flip-blue:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1) --record=true

.PHONY: flip-green
flip-green:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2) --record=true

.PHONY: flip-flop
flip-flop:
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1) --record=true
	sleep 20
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2) --record=true
	sleep 20
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1) --record=true
	sleep 20
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V2) --record=true
	sleep 20
	kubectl set image $(DEPLOY_NAME) $(IMAGE_NAME)=$(HUB_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG_V1) --record=true

.PHONY: server
server:
	kubectl apply -f $(IMAGE_NAME).yaml

.PHONY: client
client:
	source venv/bin/activate && ./client.py
