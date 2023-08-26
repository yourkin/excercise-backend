FROM python:3.11.4-bullseye

RUN mkdir -p /ex_back/
WORKDIR /ex_back

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH=/ex_back/src

RUN apt-get update \
    && apt-get -y install netcat gcc curl \
    && apt-get clean

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* ./

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# add app
COPY . /ex_back

# add entrypoint.sh
COPY ./scripts/entrypoint.sh /ex_back/scripts/entrypoint.sh
RUN chmod +x /ex_back/scripts/entrypoint.sh

WORKDIR /ex_back/src/

## run entrypoint.sh
ENTRYPOINT ["/ex_back/scripts/entrypoint.sh"]
