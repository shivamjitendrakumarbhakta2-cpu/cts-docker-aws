FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY django/requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
WORKDIR /app/django
RUN sed -i 's/\r$//g' /app/django/entrypoint.sh
RUN chmod +x /app/django/entrypoint.sh
#CMD ["sh", "-c", "/app/django/entrypoint.sh"]
ENTRYPOINT ["/app/django/entrypoint.sh"]