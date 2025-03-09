from classes.warehouse import Warehouse
from classes.deliverytruck import DeliveryTruck
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
from google.protobuf import empty_pb2

def main():
   # Create a list of delivery vehicles
   vehicles = [DeliveryTruck(vehicle_id=i) for i in range(1, 4)]  # 3 vehicles for example

   with grpc.insecure_channel('localhost:50052') as channel:
      warehouse_stub = warehouse_pb2_grpc.WarehouseServiceStub(channel)
      order_stub = order_pb2_grpc.OrderServiceStub(channel)

      # Request warehouse locations
      response = warehouse_stub.warehouseLocation(warehouse_pb2.Empty())
      print("Warehouse Coordinates:")
      for coord in response.coordinates:
         print(f"{coord.x} {coord.y}")
        
      # Order processing
      order_request = order_pb2.OrderRequest(
         order_id="order123",
         product_id="prod456",
         quantity=10,
         delivery_address="10 10"  # Example address
      )
      
      # Simulate order processing with vehicle allocation
      order_response = order_stub.processOrder(order_request)
      print(order_response.message)
      
      # Try processing another order to see vehicle locking in action
      order_request = order_pb2.OrderRequest(
         order_id="order124",
         product_id="prod457",
         quantity=5,
         delivery_address="15 15"  # Another example address
      )

      order_response = order_stub.processOrder(order_request)
      print(order_response.message)


if __name__ == '__main__':
   main()