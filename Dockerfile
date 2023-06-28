FROM mambaorg/micromamba:1.4-bullseye-slim

USER root
RUN apt update && apt install -y gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/env.yaml
# TODO: avoid installing development dependencies
RUN micromamba env create --yes -f /tmp/env.yaml && \
    micromamba clean --all --yes

EXPOSE 8501

COPY . /app
WORKDIR /app

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/opt/conda/envs/llllm-env/bin/streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
