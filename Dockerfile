FROM python:3.9-slim as builder
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r /requirements.txt

FROM debian:latest
RUN apt update && \
    apt install -y build-essential python3 python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*
COPY ./ ./
COPY --from=builder /root/.local/lib/python3.9/site-packages /usr/local/lib/python3.9/dist-packages
CMD [ "python3", "app.py" ]
EXPOSE 8000
