# Use the Makefile for easy build + run
FROM --platform=linux/amd64 python:3.11-slim-bookworm
RUN mkdir /qabot
RUN apt update
RUN apt install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh
ADD pyproject.toml /qabot/pyproject.toml
RUN cd qabot && uv sync --all-groups
# To iterate faster, we'll mount this directly into the container and edit the code there
#ADD src/ /qabot/src
ADD tests/ /qabot/tests
ADD sample_data/synthetic_dataset.csv /qabot/sample_data/synthetic_dataset.csv
WORKDIR /qabot
ENTRYPOINT ["/usr/bin/bash"]