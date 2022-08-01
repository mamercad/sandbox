.PHONY: requirements
requirements:
	poetry export --without-hashes --format=requirements.txt | tee requirements.txt
	poetry export --without-hashes --format=requirements.txt | tee docker/requirements.txt
