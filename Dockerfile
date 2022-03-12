FROM python:3.7-buster
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y cmake libdbus-glib-1-dev libgirepository1.0-dev
WORKDIR /app
ADD requirements.txt .
RUN pip3 install --user -r requirements.txt
ADD . .
CMD [ "uvicorn", "led_hack.web:app", "--host", "0.0.0.0" ]