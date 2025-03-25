FROM --platform=linux/amd64 python:3.11-slim-bookworm
RUN mkdir /qabot
ADD src/ /qabot/src
ADD tests/ /qabot/tests
ADD pyproject.toml /qabot
RUN apt update
RUN apt install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN source $HOME/.local/bin/env
RUN cd qabot
RUN uv sync
RUN uv add -e .
ENTRYPOINT ["/bin/bash"]
