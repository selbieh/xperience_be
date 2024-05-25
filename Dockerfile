FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Required to install mysqlclient with Pip
RUN apt-get update \
  && apt-get install build-dep python-psycopg2

# Install pipenv
RUN pip install --upgrade pip 

# Install application dependencies
COPY requirements.txt /app/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
RUN pip install -r requirements.txt

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000

ENTRYPOINT ["sh", "-c", "python manage.py migrate && gunicorn ecommerce.wsgi"]