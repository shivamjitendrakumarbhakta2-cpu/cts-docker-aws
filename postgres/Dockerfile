# Use the official PostgreSQL image as the base image
FROM postgres:16
COPY db_backup.sh /c2s/db_backup.sh
RUN chmod +x /c2s/db_backup.sh

COPY dumps20.sql dumps20.sql

# Set environment variables for PostgreSQL (change these as per your settings)
ENV POSTGRES_USER=mydbuser
ENV POSTGRES_PASSWORD=mydbpassword
ENV POSTGRES_DB=mydb