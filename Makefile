.PHONY: build
build:
	docker build -t mamercad/hello-python:v0.0.1 .

.PHONY: run
run: build
	docker run -d -p 6000:5000 mamercad/hello-python:v0.0.1

.PHONY: push
push: build
	docker push mamercad/hello-python:v0.0.1
