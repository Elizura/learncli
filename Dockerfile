FROM ubuntu:latest

# Install Python and dependencies
RUN apt update && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt update && \
    apt install -y python3.10 python3.10-venv python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Expose port 4000
EXPOSE 4000

# Set up the project directory
RUN mkdir /learncli
WORKDIR /learncli

# Copy project files into the container
COPY . .

RUN chmod -R 777 /learncli && \
    chown -R root:root /learncli

# Create a virtual environment and install dependencies
RUN python3.10 -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements.txt

# Set the default command
CMD ["./venv/bin/python", "/learncli/main.py"]
