from datetime import datetime

def calculate_cart_surcharge(cart_value):
    if cart_value < 1000:
        surcharge = 1000 - cart_value
    else:
        surcharge = 0

    return surcharge

def calculate_distance_surcharge(delivery_distance):
    surcharge = 200
    if delivery_distance > 1000:
        delivery_distance -= 1000

        additional = delivery_distance // 500
        remainder = delivery_distance % 500

        if remainder > 0:
            additional += 1
        
        surcharge += additional * 100

    return surcharge

def calculate_number_of_items_surcharge(number_of_items):
    if number_of_items >= 5:
        surcharge = (number_of_items - 4) * 50
        if number_of_items > 12:
            surcharge += 120
    else:
        surcharge = 0

    return surcharge

def is_rush_hour(time):
    utc_datetime = datetime.fromisoformat(time.replace("Z", "+00:00"))

    day_of_week = utc_datetime.strftime("%A")
    time_of_day = utc_datetime.strftime("%H:%M:%S")

    if day_of_week == 'Friday' and '15:00:00' <= time_of_day <= '19:00:00':
        return True
    else:
        return False
    
def calculate_final_delivery_fee(input):
    cart_value = input['cart_value']
    
    if cart_value >= 20000:
        return {'delivery_fee': 0}

    cart_surcharge = calculate_cart_surcharge(cart_value)

    delivery_distance = input['delivery_distance']
    delivery_surcharge = calculate_distance_surcharge(delivery_distance)

    number_of_items = input['number_of_items']
    number_of_items_surcharge = calculate_number_of_items_surcharge(number_of_items)

    total_delivery_fee = cart_surcharge + delivery_surcharge + number_of_items_surcharge

    time = input['time']
    rush_hour = is_rush_hour(time) # bool

    if rush_hour:
        total_delivery_fee *= 1.2

    if total_delivery_fee > 1500:
        total_delivery_fee = 1500

    return {'delivery_fee': int(total_delivery_fee)}


# helper functions
def create_test(name, input, output):
    test = {'test_name': name,
            'input': input,
            'expected_output': output}
    
    return test

def run_tests(tests, function_to_test, show_passed = False, show_failed = True):
    GREEN, RED, END = '\033[92m', '\033[91m', '\033[0m'
    GREEN_UNDERLINE, RED_UNDERLINE = '\033[92;4m', '\033[91;4m'

    total_count, passed_count, failed_count = 0, 0, 0
    failed, passed = [], []
    for i in range(len(tests)):
        test = tests[i]
        test_name = test['test_name']
        test_input = test['input']
        test_expected = test['expected_output']

        output = function_to_test(test_input)

        if output == test_expected: # passed
            passed_count += 1
            test['actual_output'] = output
            passed.append(test)

        else: # failed
            failed_count += 1
            test['actual_output'] = output
            failed.append(test)

        total_count += 1

    # end
        
    print (f'TOTAL:{total_count}, {GREEN}PASSED:{passed_count}{END}, {RED}FAILED:{failed_count}{END}')
    
    if show_passed:
        print()
        print(f'{GREEN_UNDERLINE}PASSED TESTS{END}:')

        for test in passed:
            test_name = test['test_name']
            test_input = test['input']
            test_expected = test['expected_output']
            test_actual = test['actual_output']

            print (f'Test: {test_name}')
            print (f'Input: {test_input}')
            print (f'Expected output: {test_expected}')
            print (f'Actual output: {test_actual}')
            print ()



    if failed_count == 0: # no failed tests
        return

    if show_failed: 
        print()
        print(f'{RED_UNDERLINE}FAILED TESTS{END}:')

        for test in failed:
            test_name = test['test_name']
            test_input = test['input']
            test_expected = test['expected_output']
            test_actual = test['actual_output']

            print (f'Test: {test_name}')
            print (f'Input: {test_input}')
            print (f'Expected output: {test_expected}')
            print (f'Actual output: {test_actual}')
            print ()
