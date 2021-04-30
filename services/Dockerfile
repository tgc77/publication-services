FROM python:3.9.0

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yml ./
COPY run.sh ./
RUN mkdir -p ./services
COPY __init__.py service1.py service2.py service3.py ./services/
COPY service4.py consumer.py ./services/

RUN chmod +x ./run.sh

CMD ["./run.sh"]