FROM nginx:latest

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    certbot python3-certbot-nginx \
    && apt-get clean

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

WORKDIR /usr/src/app