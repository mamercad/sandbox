NAME = "mamercad/hello-python"
TAG  = "v0.0.2"

.PHONE: blue
blue:
	kubectl set image deployment/hello-python hello-python=mamercad/hello-python:v0.0.1 --record=true

.PHONE: green
green:
	kubectl set image deployment/hello-python hello-python=mamercad/hello-python:v0.0.2 --record=true

.PHONY: k8s
k8s:
	kubectl apply -f hello-python.yaml

.PHONY: build
build:
	docker build --build-arg tag=$(TAG) -t $(NAME):$(TAG) .

.PHONY: run
run: build
	docker run -d --rm -p 6000:5000 --env tag=$(TAG) $(NAME):$(TAG)

.PHONY: push
push: build
	docker push $(NAME):$(TAG)
