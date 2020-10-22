FROM python:3

RUN apt-get update && \
    apt-get install -y nginx && \
    rm /etc/nginx/sites-enabled/default && \
    rm -rf /var/lib/apt/lists/*

ENV PORT=9090
ENV RESTAPI_ENV=prod

# Set application working directory
WORKDIR /home/src

# Install application
COPY src ./
COPY requirements.txt ./
COPY deployment/nginx/conf/restapi.conf /etc/nginx/sites-enabled/restapi.conf
COPY deployment/scripts/start.sh /start.sh

RUN pip install --no-cache-dir -r requirements.txt && \
    python manage.py db init && \
    python manage.py db migrate && \
    python manage.py db upgrade

#RUN printf "#!/bin/sh\n\n. .env/bin/activate && python manage.py runserver -h 0.0.0.0 -p ${PORT}" >> /start
RUN chmod +x /start.sh

# Run application
EXPOSE ${PORT}
ENTRYPOINT ["sh", "-c"]
CMD ["/start.sh"]