FROM python:3.7-buster
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONUNBUFFERED=1
# RUN apt-get update && apt-get install -y build-essential libdbus-glib-1-dev libgirepository1.0-dev
WORKDIR /app
ADD requirements.txt .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -qy sudo bluez
RUN printf '#!/bin/sh\ntrue\n' > /usr/local/bin/systemctl && chmod +x /usr/local/bin/systemctl
ADD . .
CMD ["./entrypoint.sh"]
