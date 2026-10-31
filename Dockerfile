FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# System packages needed for pyzbar / zbar
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libzbar0 \
        libgl1 \
        libglib2.0-0 \
    && apt-get install -y --only-upgrade ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70" \
    && python -m pip install -r requirements.txt

COPY . .

# Render provides PORT at runtime
CMD gunicorn app:app --bind 0.0.0.0:$PORT
