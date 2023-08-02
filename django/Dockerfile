FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /c2s
COPY django/requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
COPY django/entrypoint.sh /c2s/django/entrypoint.sh
RUN chmod +x /c2s/django/entrypoint.sh
EXPOSE 8000