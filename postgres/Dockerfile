# Use the official PostgreSQL image as the base image
FROM postgres:latest

RUN chmod +x db_backup.sh
CMD mkdir backup_export

# Set environment variables for PostgreSQL (change these as per your settings)
ENV POSTGRES_USER=mydbuser
ENV POSTGRES_PASSWORD=mydbpassword
ENV POSTGRES_DB=mydb