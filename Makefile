TAG := $(or ${TAG},latest)
AUTO_REPORT_IMAGE := $(or $(AUTO_REPORT_IMAGE),quay.io/edge-infrastructure/auto-report:$(TAG))

unit-test:
	pytest -vv ./tests/unit

lint:
	flake8 ./auto_report
	flake8 ./tests
	pylint ./auto_report
	pylint ./tests

build-image:
	DOCKER_BUILDKIT=1 docker build -t $(AUTO_REPORT_IMAGE) .
