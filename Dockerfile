FROM python:3.10-slim as python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base

LABEL MAINTAINER="Jonathan Farias <jonathan.developer10@gmail.com>"

RUN apt-get update && apt-get upgrade -y && apt-get install gcc g++ -y

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip wheel Cmake\
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as http-app

## Fix Timezone Error
RUN apt-get install tzdata -y && cp -r -f /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${POETRY_VENV}/bin:${PATH}:"

WORKDIR /usr/src/http_check/

RUN mkdir /usr/src/databases/

VOLUME [ "/usr/src/databases/" ]

# Copy Dependencies
COPY poetry.lock pyproject.toml /usr/src/http_check/

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache --without dev --no-root

# Copy Application
COPY ./ ./

ENV FLASK_APP=/usr/src/http_check/app.py
#ENV FLASK_DEBUG=True
#ENV FLASK_ENV=development
ENV FLASK_DEBUG=False
ENV FLASK_ENV=production

# Run Application
EXPOSE 5000:5000

#CMD [ "poetry", "run", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--cert=./keys/cert.pem", "--key=./keys/key.pem" ]

CMD [ "poetry", "run", "python3", "-m", "gunicorn", "--certfile=./keys/cert.pem", "--keyfile=./keys/key.pem", "--bind", "0.0.0.0:5000", "app:create_app()" ]