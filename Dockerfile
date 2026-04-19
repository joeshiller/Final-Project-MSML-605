FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim
# Astral image with uv preinstalled.
#3.13 to make sure we can use tensorflow

COPY scripts/container-entrypoint.sh /
RUN chmod +x /container-entrypoint.sh

RUN mkdir /work
WORKDIR /work

ENV UV_PYTHON_INSTALL_DIR=/work/.python-installs

COPY pyproject.toml /work/
COPY uv.lock /work/
COPY src /work/src
COPY scripts /work/scripts
COPY configs /work/configs
COPY README.md /work/

#No uv sync to prevent huge NVIDIA packages, use CPU-only instead
RUN uv venv && \

    . .venv/bin/activate && \

    uv pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision && \

    uv pip install facenet-pytorch kagglehub[pandas-datasets] loguru matplotlib pandas pillow pydantic scikit-learn pytest && \

    uv pip install -e . --no-deps

ENV PATH="/work/.venv/bin:$PATH"
ENTRYPOINT ["/container-entrypoint.sh"]
#No sync for CPU only
CMD ["uv", "run", "--no-sync", "python", "scripts/verify_pair.py", "--help"]