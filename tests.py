import unittest
import json
from flask import Flask
from flask.testing import FlaskClient
from delivery_calculator import (
    calculate_cart_surcharge, 
    calculate_distance_surcharge, 
    calculate_number_of_items_surcharge, 
    is_rush_hour, 
    calculate_final_delivery_fee, 
    create_test, 
    run_tests
    )
from app import app


# Tests for cart value surcharge
class CartSurchargeTests(unittest.TestCase):
    
    # Cart value more than 1000
    def test_cart_value_more_than_1000(self):
        test_input = 1001
        expected_output = 0

        result = calculate_cart_surcharge(test_input)

        self.assertEqual(result, expected_output)

    # Cart value less than 1000
    def test_cart_value_less_than_1000(self):
        test_input = 620
        expected_output = 380

        result = calculate_cart_surcharge(test_input)

        self.assertEqual(result, expected_output)

    # Cart value equal to 1000
    def test_cart_value_equal_to_1000(self):
        test_input = 1000
        expected_output = 0

        result = calculate_cart_surcharge(test_input)

        self.assertEqual(result, expected_output)    


# Tests for delivery distance surcharge
class DeliveryDistanceSurchargeTests(unittest.TestCase):
    
    # Distance less than 1000m
    def test_distance_less_than_1000(self):
        test_input = 999
        expected_output = 200

        result = calculate_distance_surcharge(test_input)

        self.assertEqual(result, expected_output)

    # Distance equal to 1000m
    def test_distance_equal_to_1000(self):
        test_input = 1000
        expected_output = 200

        result = calculate_distance_surcharge(test_input)

        self.assertEqual(result, expected_output)

    # Distance more than 1000m, not multiple of 500 (1)
    def test_distance_more_than_1000_not_multiple_1(self):
        test_input = 1001
        expected_output = 300

        result = calculate_distance_surcharge(test_input)

        self.assertEqual(result, expected_output)        

    # Distance more than 1000m, not multiple of 500 (2)
    def test_distance_more_than_1000_not_multiple_2(self):
        test_input = 2700
        expected_output = 600

        result = calculate_distance_surcharge(test_input)

        self.assertEqual(result, expected_output)   

    # Distance more than 1000m, multiple of 500
    def test_distance_more_than_1000_multiple(self):
        test_input = 3500
        expected_output = 700

        result = calculate_distance_surcharge(test_input)

        self.assertEqual(result, expected_output)   


# Tests for number of items surcharge
class NumberOfItemsSurchargeTests(unittest.TestCase):
    
    # Less than 5 items
    def test_less_than_5_items(self):
        test_input = 4
        expected_output = 0

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  

    # Exactly 5 items
    def test_exactly_5_items(self):
        test_input = 5
        expected_output = 50

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  

    # More than 5 items, not bulk
    def test_more_than_5_items_not_bulk(self):
        test_input = 8
        expected_output = 200

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  

    # Exactly 12 items, not bulk
    def test_exactly_12_items(self):
        test_input = 12
        expected_output = 400

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  

    # More than 12 items, bulk (1)
    def test_more_than_12_items_bulk_1(self):
        test_input = 13
        expected_output = 570

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  

    # More than 12 items, bulk (2)
    def test_more_than_12_items_bulk_2(self):
        test_input = 16
        expected_output = 720

        result = calculate_number_of_items_surcharge(test_input)

        self.assertEqual(result, expected_output)  


# Tests for Friday rush hour
class FridayRushHourTests(unittest.TestCase):
    
    # Not Friday, not rush hour
    def test_not_friday_not_rush_hour(self):
        test_input = "2024-01-15T13:00:00Z" # Monday, 1pm
        expected_output = False

        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output)  

    # Not Friday, yes rush hour
    def test_not_friday_yes_rush_hour(self):
        test_input = "2024-01-15T18:00:00Z" # Monday, 1pm
        expected_output = False
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output)   

    # Yes Friday, not rush hour (1, edge before) 
    def test_not_friday_not_rush_hour_before(self):
        test_input = "2024-01-19T14:59:59Z" # Friday, 2:59:59pm
        expected_output = False
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output)   

    # Yes Friday, not rush hour (2, edge after) 
    def test_not_friday_not_rush_hour_after(self):
        test_input = "2024-01-19T19:00:01Z" # Friday, 7:00:01pm
        expected_output = False
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output)  

    # Yes Friday, yes rush hour (1, edge start)
    def test_not_friday_yes_rush_hour_start(self):
        test_input = "2024-01-19T15:00:00Z" # Friday, 3pm
        expected_output = True
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output)  

    # Yes Friday, yes rush hour (2, edge end)
    def test_not_friday_yes_rush_hour_end(self):
        test_input = "2024-01-19T19:00:00Z" # Friday, 7pm sharp
        expected_output = True
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output) 

    # Yes Friday, yes rush hour (3)
    def test_not_friday_yes_rush_hour_3(self):
        test_input = "2024-01-19T18:30:12Z" # Friday, 6:30pm
        expected_output = True
    
        result = is_rush_hour(test_input)

        self.assertEqual(result, expected_output) 


# Tests for overall delivery fee (HTTP endpoint)
class DeliveryFeeEndpointTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


    # A) Example given
    def test_example_given(self):
        payload = {
            'cart_value': 790, 
            'delivery_distance': 2235, 
            'number_of_items': 3, 
            'time': '2024-01-15T13:00:00Z' # Monday, 1pm
        }
        expected_output = {'delivery_fee': 710}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)
        

    # B) Base case (cart total more than 1000, distance less than 1000m, 
    #            items less than 5, not Fri rush hour)
    def test_base_case(self):
        payload = {'cart_value': 1500, 
              'delivery_distance': 700, 
              'number_of_items': 3, 
              'time': "2024-01-12T13:00:00Z"} # Friday, 1pm
        expected_output = {'delivery_fee': 200}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)
        

    # C) Small order surcharge (cart total less than 1000)
    def test_cart_value_surcharge(self):
        payload = {'cart_value': 800, 
              'delivery_distance': 900, 
              'number_of_items': 2, 
              'time': "2024-01-11T19:00:00Z"} # Thursday, 7pm
        expected_output = {'delivery_fee': 400}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)


    # D) Distance surcharge (delivery distance more than 1000m)
    def test_delivery_distance_surcharge(self):
        payload = {'cart_value': 2000, 
              'delivery_distance': 1501, 
              'number_of_items': 4, 
              'time': "2024-01-01T16:00:00Z"} # Monday, 4pm
        expected_output = {'delivery_fee': 400}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)

    
    # E) Number of items surcharge, not bulk (5 or more items)     
    def test_number_of_items_surcharge_not_bulk(self):
        payload = {'cart_value': 1200, 
              'delivery_distance': 987, 
              'number_of_items': 7, 
              'time': "2024-01-22T15:00:00Z"} # Monday, 3pm
        expected_output = {'delivery_fee': 350}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)


    # F) Number of items surcharge, bulk (more than 12 items)
    def test_number_of_items_surcharge_bulk(self):
        payload = {'cart_value': 11000, 
              'delivery_distance': 1200, 
              'number_of_items': 16, 
              'time': "2024-01-12T13:00:00Z"} # Friday, 1pm
        expected_output = {'delivery_fee': 1020}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)

    # G) Max delivery fee
    def test_max_delivery_fee(self):
        payload = {'cart_value': 200, 
                'delivery_distance': 5000, 
                'number_of_items': 2, 
                'time': "2024-01-12T13:00:00Z"} # Friday, 1pm
        expected_output = {'delivery_fee': 1500}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)


    # H) Free delivery (cart total more than 2000)
    def test_free_delivery(self):
        payload = {'cart_value': 22000, 
              'delivery_distance': 1400, 
              'number_of_items': 7, 
              'time': "2024-01-12T13:00:00Z"} # Friday, 1pm
        expected_output = {'delivery_fee': 0}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)

    # I) Friday rush hour
    def test_rush_hour(self):
        payload = {'cart_value': 1800, 
              'delivery_distance': 1100, 
              'number_of_items': 7, 
              'time': "2024-01-12T17:00:00Z"} # Friday, 5pm
        expected_output = {'delivery_fee': 540}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)

    # J) Friday rush hour,  max delivery fee
    def test_rush_hour_max_delivery_fee(self):
        payload = {'cart_value': 2700, 
              'delivery_distance': 2700, 
              'number_of_items': 19, 
              'time': "2024-01-12T19:00:00Z"} # Friday, 7pm
        expected_output = {'delivery_fee': 1500}

        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)

    # K) Friday rush hour, free delivery
    def test_rush_hour_free_delivery(self):
        payload = {'cart_value': 21700, 
              'delivery_distance': 1600, 
              'number_of_items': 15, 
              'time': "2023-12-22T18:00:00Z"} # Friday, 6pm
        expected_output = {'delivery_fee': 0}
        
        response = self.app.post('/calculate_delivery_fee', json=payload)
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected_output)



if __name__ == '__main__':
    unittest.main()