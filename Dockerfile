# Use the official Python image
FROM python:3.10-slim

# Set up the project directory
RUN mkdir /learncli

# Set the working directory
WORKDIR /learncli

# Copy project files into the container
COPY . .

# Define a volume for the SQLite database
VOLUME ["/learncli"]

# Install dependencies
RUN pip install -r requirements.txt

# Set the default command
CMD ["python", "/learncli/main.py"]
