FROM ubuntu:latest

RUN apt update && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.10

RUN apt install -y python3-pip && apt clean && pip install --upgrade pip==24.0

WORKDIR /learncli

COPY . /learncli

RUN pip install -r /learncli/requirements.txt

CMD ["python3", "main.py"]