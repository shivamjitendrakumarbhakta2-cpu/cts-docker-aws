FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /c2s
WORKDIR /c2s
RUN apt-get update \
    && apt-get install -y netcat
COPY requirements.txt /c2s/
RUN pip install -r requirements.txt
COPY . /c2s/
ENV DJANGO_SETTINGS_MODULE=myproject.settings.production
EXPOSE 8000
ENTRYPOINT ["/c2s/django/entrypoint.sh"]
