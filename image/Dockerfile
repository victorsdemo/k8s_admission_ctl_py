FROM python:3.9.16-slim

RUN apt-get update -y && apt-get install -y python3-pip
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY admissioncontroller.py /app
COPY wsgi.py /app

# create the app user
RUN addgroup --gid 11000 app && useradd --uid 11000 --gid app -d /app -m -s/bin/bash  -c k8s-admctl,9876543210,securecon app
# chown all the files to the app user
RUN chown -R app:app /app
# change to the app user
USER app

CMD gunicorn --certfile=/certs/webhook.crt --keyfile=/certs/webhook.key --bind 0.0.0.0:8443 wsgi:webhook