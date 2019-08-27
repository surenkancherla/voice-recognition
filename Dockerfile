# Use an official Python runtime as a parent image
#FROM python:3.6-slim
FROM akbdasdocker/avconv

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

#RUN apt-get update && apt-get install -y python-pip

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Install any needed packages specified in requirements.txt


# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
COPY app.py .
CMD ["python", "app.py"]

