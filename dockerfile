FROM python:3.11-alpine

RUN apk update
RUN apk add gcc libc-dev libffi-dev libsodium-dev python3-dev

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]
