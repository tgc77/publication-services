FROM python:3.9.0

RUN apt-get update && apt-get -y install netcat && apt-get clean
WORKDIR /client
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY config.yml ./
COPY run.sh ./
COPY app.py ./
RUN mkdir -p ./app
COPY app/ ./app/
RUN chmod +x ./run.sh
EXPOSE 5000
CMD ["./run.sh"]