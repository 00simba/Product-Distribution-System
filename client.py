from classes.warehouse import Warehouse
from classes.truck import Truck
from classes.order import Order
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
from google.protobuf import empty_pb2
import math
import threading 

warehouses = []
orders = []
trucks = []

def calculate_distance(order_x, order_y):
   
   # distance formula d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

   distance = float('inf')

   distances = []

   for warehouse in warehouses:

         warehouse_x = float(warehouse.x)
         warehouse_y = float(warehouse.y)

         order_x = float(order_x)
         order_y = float(order_y)

         distance = math.sqrt((warehouse_x - order_x)**2 + (warehouse_y - order_y)**2)
         distances.append((int(warehouse.id), distance))

   distances.sort(key=lambda x:x[1])
   return distances
   
def process_order(x, y, quantity):
   
   distances = calculate_distance(x, y)
   print(quantity)


def main():

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      warehouseStub = warehouse_pb2_grpc.WarehouseServiceStub(channel)
      response = warehouseStub.warehouseInformation(warehouse_pb2.Empty())
      for warehouse in response.warehouseInfo:
        warehouses.append(Warehouse(warehouse.id, warehouse.x, warehouse.y, warehouse.capacity))
        # Each warehouse will have one truck with a volume of 20 cubic meters
        trucks.append(Truck(warehouse.id, 20, False))


      orderStub = order_pb2_grpc.OrderServiceStub(channel)
      response = orderStub.orderInformation(order_pb2.OrderEmpty())
      for order in response.orderInfo:
         orders.append(Order(order.x, order.y, order.quantity))


if __name__ == '__main__':
   
   main()

   threads = list()

   for order in orders:
      x = threading.Thread(target=process_order, args=(order.x, order.y, order.quantity))
      threads.append(x)
      x.start()

   for thread in threads:
      thread.join()