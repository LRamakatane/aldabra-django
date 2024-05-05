FROM python:3.9
ENV PYTHONUNBUFFERED 1

# Update and install build essentials
RUN apt-get update && apt-get install -y build-essential && apt install python3-dev libpq-dev -y

WORKDIR /app

#Install dependencies
COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --upgrade setuptools
RUN pip3 install --force-reinstall -r requirements.txt

# Copy the rest of the application
COPY . .

# Set enironment variables

# ENV ENV=dev
# ENV SECRET_KEY="47c9d747bd60e375bc8656a9f64a246cf65a0bd9c88d727122a82050e38f7fa08b799f731a61705c41c6053c57935fee"

# Set the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]