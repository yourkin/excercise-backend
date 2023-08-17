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

Additionally, tests are included and documentation on how to test the application as a whole and its pieces.

A `solution.md` file documents the decisions, assumptions, and also improvements that might be incorporated in the future.

### Bonus tasks
* How would the system change if we would receive a high volume of async updates to the orders placed through a socket connection on the stock exchange, e.g. execution information? The changes are outlined in the `solution.md`.

## Code quality

In order to keep a certain amount of code quality, we are using pre-commit hooks
in this repository, which are installed by a 3rd-party tool called [pre-commit](https://pre-commit.com/).
