FROM python:3.10-slim

RUN mkdir /learncli && chmod 000 /learncli

WORKDIR /learncli

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["python", "/learncli/main.py"]
