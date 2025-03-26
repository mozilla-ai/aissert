# docker image build -t qabot -f Dockerfile .
# docker run -it --name qabot qabot
# docker start -i qabot
FROM --platform=linux/amd64 python:3.11-slim-bookworm
RUN mkdir /qabot
ADD src/ /qabot/src
ADD tests/ /qabot/tests
ADD pyproject.toml /qabot
ADD sample_data/synthetic_dataset.csv /qabot/sample_data/synthetic_dataset.csv
RUN apt update
RUN apt install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh
RUN cd qabot && uv sync
ENTRYPOINT ["/bin/bash"]
# then uv pip install pytest
