FROM python:3.10-alpine as python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base

LABEL MAINTAINER="Jonathan Farias <jonathan.developer10@gmail.com>"

RUN apk --update --no-cache add gcc g++ 

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip wheel Cmake\
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as http-app

## Fix Timezone Error
RUN apk add --no-cache tzdata && cp -r -f /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /usr/src/http_check/

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache --without dev --no-root

# Copy Application
COPY . ./

ENV FLASK_APP=/usr/src/http_check/app.py

ENV FLASK_DEBUG=True

# Run Application
EXPOSE 5000:5000

CMD [ "poetry", "run", "python3", "-m", "flask", "run", "--host=0.0.0.0" ]