FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
# Install pip
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --upgrade pip && \
    apt-get clean

# Install dependencies
RUN pip install prompt_toolkit
WORKDIR /app
COPY questions.py /app
CMD ["python3", "/app/questions.py"]