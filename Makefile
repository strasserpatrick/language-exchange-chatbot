install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-infra:
	pip install -r requirements-infra.txt

install-all:
	pip install -r requirements.txt -r requirements-dev.txt -r requirements-infra.txt

format:
	black --line-length 88 .
	isort --profile black  --line-length 88 .
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .

lint:
	flake8 --max-line-length 88 .

streamlit:
	streamlit run src/frontend/streamlit_application.py

plan:
	cdktf diff

deploy:
	cdktf deploy

build: 
	export DOCKER_DEFAULT_PLATFORM=linux/amd64
	docker compose build 
