.DEFAULT_GOAL = build

.PHONY: requirements
requirements:
	poetry export --without-hashes --format=requirements.txt | tee requirements.txt

.PHONY: build
build: requirements
	docker build --tag ghcr.io/mamercad/sandbox:latest .

.PHONY: push
push: push
	docker push ghcr.io/mamercad/sandbox:latest
