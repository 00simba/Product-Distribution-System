from flask import Flask, request, jsonify
import json
from rabbitmq_config import setup_exchange_and_queue, publish_stock_update
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_warehouse_data():
    warehouse_info = []
    with open("./files/warehouse.txt", "r") as f:
        for line in f:
            values = line.split()
            warehouse_info.append({
                "id": values[0],
                "x": values[1],
                "y": values[2],
                "capacity": values[3],
                "coverage": values[4],
                "stock": values[-2]
            })
    return warehouse_info

def read_order_data():
    order_info = []
    with open("./files/orders.txt", "r") as f:
        for line in f:
            values = line.split()
            order_info.append({
                "id": values[0],
                "x": values[1],
                "y": values[2],
                "quantity": values[3]
            })
    return order_info

@app.route('/warehouse/info', methods=['GET'])
def get_warehouse_info():
    try:
        warehouse_info = read_warehouse_data()
        return jsonify({"warehouses": warehouse_info})
    except Exception as e:
        logger.error(f"Error reading warehouse info: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/order/info', methods=['GET'])
def get_order_info():
    try:
        order_info = read_order_data()
        return jsonify({"orders": order_info})
    except Exception as e:
        logger.error(f"Error reading order info: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stock/update', methods=['POST'])
def update_stock():
    try:
        data = request.get_json()
        if not data or 'updates' not in data:
            return jsonify({"error": "Invalid request format"}), 400

        updates = data['updates']
        new_lines = []
        failed_updates = []

        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                cur_line = line.split()
                warehouse_id = cur_line[0]
                if warehouse_id in updates:
                    old_stock = int(cur_line[-2])
                    update_amount = int(updates[warehouse_id])
                    
                    # Calculate new stock and ensure it doesn't go below 0
                    new_stock = max(0, old_stock - update_amount)
                    
                    # Only update if we have sufficient stock
                    if old_stock >= update_amount:
                        cur_line[-2] = str(new_stock)
                        # Publish stock update to RabbitMQ
                        publish_stock_update(warehouse_id, old_stock, new_stock)
                        logger.info(f"Updated warehouse {warehouse_id}: {old_stock} -> {new_stock}")
                    else:
                        failed_updates.append({
                            "warehouse_id": warehouse_id,
                            "requested": update_amount,
                            "available": old_stock
                        })
                        logger.warning(f"Insufficient stock in warehouse {warehouse_id}: {old_stock} < {update_amount}")
                new_lines.append(cur_line)

        with open('./files/warehouse.txt', "w") as f:
            for line in new_lines:
                f.write(" ".join(line) + "\n")

        response = {
            "message": "Successfully updated warehouse stock",
            "failed_updates": failed_updates
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error updating stock: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stock/info', methods=['GET'])
def get_stock_info():
    try:
        stock_info = []
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                stock_info.append({
                    "warehouse_id": values[0],
                    "warehouse_stock": values[-2]
                })
        return jsonify({"stock_info": stock_info})
    except Exception as e:
        logger.error(f"Error reading stock info: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Setup RabbitMQ exchange and queue
    setup_exchange_and_queue()
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=50052)