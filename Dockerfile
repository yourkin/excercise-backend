FROM python:3.11.4-bullseye as builder

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat \
#    gcc curl \
    && apt-get clean

RUN mkdir -p /excercise/
WORKDIR /excercise

# Install poetry
RUN pip install poetry

COPY . /excercise

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


# Build the project and output the .whl file to the dist/ folder
RUN poetry build

## Here we start a new build stage so that final image does not contain poetry tooling and python bytecode (.pyc)
#FROM python:3.11.4-bullseye as runner
#
## Set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /excercise
#
## Here we copy from the "builder" stage only the libraries installed
#COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
#
## Copy the built .whl file from the builder stage
#COPY --from=builder /app/dist/*.whl /excercise/

# Install the package using pip
RUN pip install /excercise/dist/*.whl

# add entrypoint.sh
COPY ./entrypoint.sh /excercise/entrypoint.sh
RUN chmod +x /excercise/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/excercise/entrypoint.sh"]
