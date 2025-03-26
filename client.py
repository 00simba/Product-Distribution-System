import requests
import json
import logging
import math
import time
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WarehouseClient:
    def __init__(self, base_url="http://localhost:50052"):
        self.base_url = base_url
        self.warehouses = []
        self.orders = []
        self.trucks = []
        self.stock_map = {}
        self.visited = set()
        self.unfulfilled = []

    def get_warehouse_info(self):
        """Get all warehouse information"""
        try:
            response = requests.get(f"{self.base_url}/warehouse/info")
            response.raise_for_status()
            return response.json()["warehouses"]
        except Exception as e:
            logger.error(f"Error getting warehouse info: {str(e)}")
            raise

    def get_order_info(self):
        """Get all order information"""
        try:
            response = requests.get(f"{self.base_url}/order/info")
            response.raise_for_status()
            return response.json()["orders"]
        except Exception as e:
            logger.error(f"Error getting order info: {str(e)}")
            raise

    def update_stock(self, updates):
        """Update warehouse stock
        Args:
            updates (dict): Dictionary of warehouse_id to quantity to subtract
        """
        try:
            response = requests.post(
                f"{self.base_url}/stock/update",
                json={"updates": updates}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error updating stock: {str(e)}")
            raise

    def get_stock_info(self):
        """Get current stock information"""
        try:
            response = requests.get(f"{self.base_url}/stock/info")
            response.raise_for_status()
            return response.json()["stock_info"]
        except Exception as e:
            logger.error(f"Error getting stock info: {str(e)}")
            raise

    def calculate_distance(self, order_x, order_y):
        """Calculate distances to warehouses within coverage"""
        distances = []
        for warehouse in self.warehouses:
            warehouse_x = float(warehouse["x"])
            warehouse_y = float(warehouse["y"])
            warehouse_coverage = float(warehouse["coverage"])
            order_x = float(order_x)
            order_y = float(order_y)

            distance = math.sqrt((warehouse_x - order_x)**2 + (warehouse_y - order_y)**2)
            if distance <= warehouse_coverage:
                distances.append((int(warehouse["id"]), distance))

        distances.sort(key=lambda x: x[1])
        return distances

    def check_stock(self, warehouse_id, quantity):
        """Check if warehouse has sufficient stock"""
        stock_info = self.get_stock_info()
        for stock in stock_info:
            if int(warehouse_id) == int(stock["warehouse_id"]):
                current_stock = int(stock["warehouse_stock"])
                return current_stock >= int(quantity)
        return False

    def process_order(self, order_id, x, y, quantity):
        """Process a single order"""
        distances = self.calculate_distance(x, y)
        curr_quantity = int(quantity)
        order_fulfilled = False

        while curr_quantity > 0:
            for warehouse_id, _ in distances:
                delivery_quantity = min(20, curr_quantity)
                if self.check_stock(warehouse_id, delivery_quantity):
                    # Get current stock before updating
                    stock_info = self.get_stock_info()
                    current_stock = 0
                    for stock in stock_info:
                        if int(warehouse_id) == int(stock["warehouse_id"]):
                            current_stock = int(stock["warehouse_stock"])
                            break
                    
                    # Only update if it won't go below 0
                    if current_stock >= delivery_quantity:
                        # Update stock for this delivery
                        if warehouse_id in self.stock_map:
                            new_total = int(self.stock_map[warehouse_id]) + delivery_quantity
                            if new_total <= current_stock:  # Ensure we don't exceed current stock
                                self.stock_map[warehouse_id] = str(new_total)
                            else:
                                continue  # Skip this warehouse if update would exceed stock
                        else:
                            self.stock_map[warehouse_id] = str(delivery_quantity)

                        print(f"Order {order_id} - Warehouse {warehouse_id} - Quantity: {delivery_quantity}")
                        time.sleep(1)  # Simulate delivery time
                        curr_quantity -= delivery_quantity
                        order_fulfilled = True
                        break
            else:
                # No warehouse could fulfill the remaining quantity
                if not order_fulfilled:
                    self.unfulfilled.append({"id": order_id, "quantity": curr_quantity})
                break

def main():
    # Create client instance
    client = WarehouseClient()
    
    try:
        # Get warehouse information
        client.warehouses = client.get_warehouse_info()
        print("\nWarehouse Information:")
        print(json.dumps(client.warehouses, indent=2))
        
        # Get order information
        client.orders = client.get_order_info()
        print("\nOrder Information:")
        print(json.dumps(client.orders, indent=2))
        
        # Process orders concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    client.process_order,
                    order["id"],
                    order["x"],
                    order["y"],
                    order["quantity"]
                ) for order in client.orders
            ]
            concurrent.futures.wait(futures)
        
        # Update warehouse stock
        if client.stock_map:
            print("\nUpdating warehouse stock...")
            print("Stock updates to be applied:", json.dumps(client.stock_map, indent=2))
            update_result = client.update_stock(client.stock_map)
            print("Stock Update Result:")
            print(json.dumps(update_result, indent=2))
        
        # Report unfulfilled orders
        if client.unfulfilled:
            print("\nUnfulfilled Orders:")
            print(json.dumps(client.unfulfilled, indent=2))
        else:
            print("\nAll orders fulfilled successfully!")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()

