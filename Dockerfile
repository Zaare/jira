FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Install necessary packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy and install requirements
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Add entrypoint script
RUN chmod +x /code/entrypoint.sh

# Expose the port on which the Django app will run
EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
