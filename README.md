# Backend engineering exercise

### Intro 

The "start" branch of the repository contains a bare setup for a REST API to place orders via a `POST - /orders` request, it can be found in [./app/api.py](src/ex_back/api/v1/router.py).
Additionally, it contains [a building block](src/ex_back/core/stock_exchange.py) that symbolizes placing an order at the stock exchange.

The folder [tests](./tests) contains the setup for tests with the framework pytest.

The challenge is to implement the missing parts in the API and to make it scalable and reliable for a high volume of requests applying modern software engineering principles.  

## Main task

We finalize the missing parts in this repository so that the following requirements are fulfilled:
1. a valid request to `POST /orders` should result in the order being stored in a database of your choice.
2. the created order should be placed at the stock exchange (use the method `place_order` provided in stock_exchange.py)
3. the endpoint should return a status code of 201 and the created order details, in case that: the order has been saved in the database **AND** it is **guaranteed** that the order is being placed on the stock exchange.  
4. in case of an error in the endpoint it should return the status code 500 and the body `{"message": "Internal server error while placing the order"}` 
5. the API should be highly scalable and reliable. The reliability of the provided stock exchange should not impact the reliability of the `POST /orders` endpoint


Additionally, tests and documentation on how to test the application as a whole and its pieces.

A `solution.md` file documents the decisions, assumptions, and also improvements that might be incorporated in the future.

## Environment variables

Before running the application, environment variables must be set in the .env file. An example of the .env file can be found in the .env.example file.

## Running the application

The application can be run locally in development mode by executing the `run.sh` script in the root directory of the repository.
Depending on the environment variables set, the application will run the development server on port 8000 or production server on port 80.
Navigate to /docs to see the API documentation.

## Running tests

Running the tests locally is as simple as running the `run_tests.sh` script in the root directory of the repository.

## Code quality

In order to keep a certain amount of code quality, we are using pre-commit hooks
in this repository, which are installed by a 3rd-party tool called [pre-commit](https://pre-commit.com/).

## Branches

The repository contains branches that each represent a distinct approach to the problem, use different technologies, or are in different stages of development.

### Current branch

`event-sourcing/rabbitmq-celery-redis` 

This branch implements event-sourcing with the transactional outbox pattern using RabbitMQ, Celery, and Redis. The application architecture leverages RabbitMQ for event publishing, Celery for asynchronous task execution, and Redis for caching, concurrency management, and task queuing. Event sourcing, a design pattern, is employed to capture and persist all changes to the application state as a sequence of immutable events. This approach provides a reliable audit trail of past actions, enabling data consistency, auditing, and the ability to reconstruct application state from historical events. 