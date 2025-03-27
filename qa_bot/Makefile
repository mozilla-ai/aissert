# Variables
IMAGE_NAME = qabot
DOCKERFILE = Dockerfile
CONTAINER_NAME = qabot
VOLUME_MOUNT = $(PWD)/src:/qabot/src
DATA_MOUNT = $(PWD)/sample_data:/qabot/sample_data
OUT_MOUNT = $(PWD)/outputs:/qabot/outputs


# Targets
.PHONY: build run

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

run:
	@echo "Running Docker container..."
	docker run \
		-v $(VOLUME_MOUNT) \
		-v $(DATA_MOUNT) \
		-v $(OUT_MOUNT) \
		-e MISTRAL_API_KEY=$(MISTRAL_API_KEY) \
		-it --name $(CONTAINER_NAME) $(IMAGE_NAME)

report:
	@echo "Checking if container $(CONTAINER_NAME) is running..."
	docker run \
		-v $(VOLUME_MOUNT) \
		-v $(DATA_MOUNT) \
		-v $(OUT_MOUNT) \
		-e MISTRAL_API_KEY=$(MISTRAL_API_KEY) -it --rm --name $(CONTAINER_NAME)_test $(IMAGE_NAME) \
		bash -c "uv run python src/manual_report.py"

test:
	@echo "Running tests in Docker container..."
	docker run \
		-v $(VOLUME_MOUNT) \
		-v $(DATA_MOUNT) \
		-v $(OUT_MOUNT) \
		-e MISTRAL_API_KEY=$(MISTRAL_API_KEY) -it --rm \
		--name $(CONTAINER_NAME)_test $(IMAGE_NAME) \
		bash -c "uv run pytest"

clean:
	@echo "Removing container $(CONTAINER_NAME)..."
	-@docker rm -f $(CONTAINER_NAME) || echo "Container $(CONTAINER_NAME) does not exist or could not be removed."