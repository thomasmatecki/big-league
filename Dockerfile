FROM node:16.13.2-bullseye

WORKDIR /app

COPY ./web /app
RUN npm install
ENTRYPOINT npm