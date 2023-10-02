FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
RUN apk add --update npm
RUN apk update && apk add gcc musl-dev libffi-dev
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
WORKDIR "/app/app/static/js"
RUN npm install