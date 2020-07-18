HUB_NAMESPACE  = "mamercad"
IMAGE_NAME     = "hello-python"
IMAGE_TAG      = "blue"
DEPLOY_NAME    = "deployment/hello-python"
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

.PHONE: blue
blue:
	kubectl set image $(DEPLOY_NAME) hello-python=$(HUB_NAMESPACE)/$(IMAGE_NAME):blue --record=true

.PHONE: green
green:
	kubectl set image $(DEPLOY_NAME) hello-python=$(HUB_NAMESPACE)/$(IMAGE_NAME):green --record=true

.PHONY: k8s
k8s:
	kubectl apply -f $(IMAGE_NAME).yaml
