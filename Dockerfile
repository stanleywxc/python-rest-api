FROM python:3

# Set application working directory
WORKDIR /usr/src
# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install application
COPY src ./

# Run application
CMD ["python", "manage.py run"]