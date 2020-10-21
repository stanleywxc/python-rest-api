FROM python:3

# Set application working directory
WORKDIR /usr/src

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install application
COPY src ./

ENV PORT=9191

RUN printf "#!/bin/sh\n\npython manage.py runserver -h 0.0.0.0 -p ${PORT}" >> /start
RUN chmod +x /start

# Run application
EXPOSE ${PORT}
ENTRYPOINT ["sh", "-c"]
CMD ["/start"]