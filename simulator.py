import random
import time
from datetime import datetime

# Sample Products list
products = [
    {"id": "P101", "name": "Milka Chocolate", "unit_weight": 100},
    {"id": "P102", "name": "Lay's Chips", "unit_weight": 50},
    {"id": "P103", "name": "Coke Can", "unit_weight": 330},
    {"id": "P104", "name": "Badam Milk", "unit_weight": 200}
]

def generate_sensor_log():
    product = random.choice(products)
    # Action: 1 = Item Picked/Touched, 0 = Restocked
    action = random.choices(["Picked", "Restocked", "Touched (Put Back)"], weights=[0.5, 0.3, 0.2])[0]
    
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product_id": product["id"],
        "product_name": product["name"],
        "action": action,
        "weight_delta": product["unit_weight"] if action == "Picked" else -product["unit_weight"]
    }
    return log

if __name__ == "__main__":
    print("Starting Smart Shelf IoT Simulator... Press Ctrl+C to stop.")
    while True:
        log = generate_sensor_log()
        print(log)
        # Append log to a CSV file to act as our database
        with open("shelf_logs.csv", "a") as f:
            f.write(f"{log['timestamp']},{log['product_id']},{log['product_name']},{log['action']},{log['weight_delta']}\n")
        time.sleep(3)