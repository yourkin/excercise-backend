FROM python:3.11.4-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc curl \
    && apt-get clean

# Use the new PEP 518 recommended method
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

#
## Copy only requirements, to cache them in docker layer
#COPY poetry.lock pyproject.toml /app/
#
## Project initialization:
#RUN poetry config virtualenvs.create false \
#  && poetry install --no-interaction --no-ansi
#
## Copy poetry.lock* in case it doesn't exist in the repo
#COPY ./pyproject.toml ./poetry.lock* ./
#
## Allow installing dev dependencies to run tests
#ARG INSTALL_DEV=true
#RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# add app
COPY . /app

# Install poetry
RUN pip install poetry

# Build the Python package
RUN poetry build

# Install the Python package
RUN pip install dist/exercise_backend*.whl

# add entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
