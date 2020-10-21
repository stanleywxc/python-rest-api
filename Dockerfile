FROM python:3

# Set application working directory
WORKDIR /usr/src
# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install application
COPY src ./

# Run application
EXPOSE 9191
ENTRYPOINT ["sh", "-c"]
CMD ["python", "manage.py runserver -h 0.0.0.0 -p 9191"]