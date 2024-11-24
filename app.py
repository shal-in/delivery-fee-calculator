from flask import Flask, request, jsonify
from delivery_calculator import (
    calculate_cart_surcharge, 
    calculate_distance_surcharge, 
    calculate_number_of_items_surcharge, 
    is_rush_hour, 
    calculate_final_delivery_fee
    )

app = Flask(__name__)

@app.route('/calculate_delivery_fee', methods = ['POST'])
def calculate_delivery_fee():
    data = request.get_json()

    delivery_fee = calculate_final_delivery_fee(data)
    
    return jsonify(delivery_fee)


if __name__ == '__main__':
    app.run(port=4040, debug=True)