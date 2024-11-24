# Wolt Internship Assigment - Backend

## Overview

The Delivery Fee Calculator is a Flask-based application designed to calculate delivery fees based on various factors, such as cart value, delivery distance, number of items, and rush hours. This README provides a detailed guide on the project's structure, usage, core functions, testing procedures, and example scenarios.

## Table of Contents

- [Wolt Internship Assigment - Backend](#wolt-internship-assigment---backend)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Running the Application](#running-the-application)
  - [Example Usage](#example-usage)
  - [Core Functions](#core-functions)
    - [calculate\_cart\_surcharge](#calculate_cart_surcharge)
    - [calculate\_distance\_surcharge](#calculate_distance_surcharge)
    - [calculate\_number\_of\_items\_surcharge](#calculate_number_of_items_surcharge)
    - [is\_rush\_hour](#is_rush_hour)
    - [calculate\_final\_delivery\_fee](#calculate_final_delivery_fee)
  - [Unit Tests](#unit-tests)

## Project Structure

The project follows a standard structure:

- **app.py:** Flask server implementation
- **delivery_calculator.py:** Core functions for calculating delivery fees
- **tests.py:** Unit tests for the delivery calculator functions
- **README.md:** Project documentation
- **examples_calculations.pdf:** Scanned pages showing the output of example cases

## Running the Application

To run the application, follow these steps:

1. Install dependencies: 
    ```bash 
   pip install Flask
    ```
2. Run the server:
    ```bash
   python app.py
    ```
3. Access the API at `http://localhost:4040/calculate_delivery_fee` using a POST request with JSON payload. See below for example usage.

## Example Usage
```bash
import requests

url = "http://localhost:4040/calculate_delivery_fee"

payload = {
    "cart_value": 1500,
    "delivery_distance": 700,
    "number_of_items": 3,
    "time": "2024-01-12T13:00:00Z"
}

response = requests.post(url, json=payload)
print(response.json()) # should print {'delivery_fee': 200}
```

## Core Functions

The overall delivery fee calculator uses four smaller functions which deal with each aspect of the delivery fee (cart value, distance, number of items, and rush hour) individually. The descriptions, as well as any special considerations, for each function is listed below. 

### calculate_cart_surcharge

- Description: Calculates surcharge based on cart value.
- Signature: `calculate_cart_surcharge(cart_value) -> surcharge`

### calculate_distance_surcharge

- Description: Calculates surcharge based on delivery distance.
- Signature: `calculate_distance_surcharge(delivery_distance) -> surcharge`

### calculate_number_of_items_surcharge

- Description: Calculates surcharge based on the number of items.
- Signature: `calculate_number_of_items_surcharge(number_of_items) -> surcharge`

### is_rush_hour

- Description: Checks if the delivery time is during rush hours.
- Signature: `is_rush_hour(time) -> bool`
- Regarding rush hour timings on Fridays, the instructions didn't explicitly specify whether it concludes at 18:59:59 or 19:00:00. To address this minor ambiguity, I've defined rush hour as the period from 15:00:00 to 19:00:00 on Fridays, inclusive.

### calculate_final_delivery_fee

- Description: Combines surcharges and adjusts for rush hours to get the final delivery fee.
- Signature: `calculate_final_delivery_fee(input) -> {'delivery_fee': int}`

## Unit Tests
The `tests.py` file contains a comprehensive set of unit tests to ensure the accuracy of the delivery calculator functions. Each individual part of the delivery calculator has been tested. The working out for the overall delivery fee calculations (Examples A-K) are included in the `examples_calculations.pdf` document.

To run the tests, execute the following command in the terminal:
```bash
python tests.py
```

Note: The test suite utilizes the `unittest` module, which is part of the Python standard library. You don't need to install it separately; it comes bundled with Python.