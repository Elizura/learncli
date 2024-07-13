FROM ubuntu:latest

RUN apt update && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.10 python3.10-venv python3-pip

EXPOSE 4000

RUN mkdir /learncli && chmod 000 /learncli
WORKDIR /learncli

COPY . .

RUN python3.10 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip==24.0 && \
    pip install -r /learncli/requirements.txt

CMD ["/learncli/venv/bin/python", "/learncli/main.py"]

WORKDIR /playground