FROM python:latest
RUN apt-get -y update
RUN mkdir -p /app/my-bot
WORKDIR /app/my-bot
COPY ./ /app/my-bot
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT python /app/my-bot/launcher.py