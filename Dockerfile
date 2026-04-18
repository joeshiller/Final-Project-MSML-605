FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
# ^--- Astral's Docker image that has UV installed.

COPY scripts/container-entrypoint.sh /

RUN mkdir /work
WORKDIR /work

ENV UV_PYTHON_INSTALL_DIR=/work/.python-installs

ENTRYPOINT ["/container-entrypoint.sh"]
CMD ["uv", "run", "scripts/benchmark.py"]
