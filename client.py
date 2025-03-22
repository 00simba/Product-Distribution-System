from classes.warehouse import Warehouse
from classes.truck import Truck
from classes.order import Order
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
import updatestock_pb2
import updatestock_pb2_grpc
import getstock_pb2
import getstock_pb2_grpc
import math
import time
import concurrent.futures

warehouses = []
orders = []
trucks = []
stock_map = {}
visited = set()
unfulfilled = []

def calculate_distance(order_x, order_y):
   
   # distance formula d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

   distance = float('inf')
   distances = []

   for warehouse in warehouses:
         warehouse_x = float(warehouse.x)
         warehouse_y = float(warehouse.y)
         warehouse_coverage = float(warehouse.coverage)

         order_x = float(order_x)
         order_y = float(order_y)

         distance = math.sqrt((warehouse_x - order_x)**2 + (warehouse_y - order_y)**2)
         if(distance <= warehouse_coverage):
            distances.append((int(warehouse.id), distance))

   distances.sort(key=lambda x:x[1])
   return distances

def map_to_proto(map):
   
   hash_map = updatestock_pb2.HashMap()

   for k, v in map.items():
      entry = hash_map.entries.add()
      entry.key = str(k)
      entry.value = str(v)

   return hash_map

def update_warehouse_stock(stock_map):

   print("requesting stock update from server...")

   map_proto = map_to_proto(stock_map)

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      updateStub = updatestock_pb2_grpc.UpdateWarehouseServiceStub(channel)
      response = updateStub.updateStock(map_proto)
      print(f"response from server: {response.message}")

def check_stock(id, quantity):

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      stockStub = getstock_pb2_grpc.GetWarehouseServiceStub(channel)
      response = stockStub.getStock(getstock_pb2.StockEmpty())
      for stock in response.stockInfo:
         if int(id) == int(stock.warehouse_id) and int(quantity) <= int(stock.warehouse_stock):
            return 1

      return 0

   
def process_order(order_id, x, y, quantity):
   
   # each distance is (warehouse_id, distance) for that order
   distances = calculate_distance(x, y)
   curr_quantity = int(quantity)

   while len(orders):

      for distance in distances:

         truck = trucks[distance[0] - 1]
         warehouse_id = truck.id    

         if check_stock(warehouse_id, quantity) == 0:
            visited.add((order_id, warehouse_id))


         if not (truck.is_active) and check_stock(warehouse_id, quantity):

            # carry out delivery

            truck.is_active = True
            order_chunk = 1

            while curr_quantity // 20 != 0:

               # each chunk is 20
               if truck.id in stock_map:
                  stock_map[truck.id] = stock_map.get(truck.id) + 20
               else:
                  stock_map[truck.id] = 20

               print(f"order {order_id} - truck {truck.id} - chunck {order_chunk}: delivery time {curr_quantity//20} days")
               time.sleep(int(curr_quantity)//20)
               order_chunk += 1
               curr_quantity -= 20


            for index, order in enumerate(orders):
               if int(order.id) == int(order_id):
                  orders.pop(index)

            truck.is_active = False

      if check_stock(warehouse_id, order_id) == 0 and (order_id, warehouse_id) in visited:
         for index, order in enumerate(orders):
               if int(order.id) == int(order_id):
                  unfulfilled.append(order)
                  orders.pop(index)



def main():

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      warehouseStub = warehouse_pb2_grpc.WarehouseServiceStub(channel)
      response = warehouseStub.warehouseInformation(warehouse_pb2.Empty())
      for warehouse in response.warehouseInfo:
        warehouses.append(Warehouse(warehouse.id, warehouse.x, warehouse.y, warehouse.capacity, warehouse.coverage))
        # each warehouse will have one truck with a volume of 20 cubic meters
        trucks.append(Truck(warehouse.id, 20, False))


      orderStub = order_pb2_grpc.OrderServiceStub(channel)
      response = orderStub.orderInformation(order_pb2.OrderEmpty())
      for order in response.orderInfo:
         orders.append(Order(order.id, order.x, order.y, order.quantity))


if __name__ == '__main__':
   
   main()

   with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = [executor.submit(process_order, order.id, order.x, order.y, order.quantity) for order in orders]
      
   # update warehouse stock quantity - truck.id maps to warehouse.id
   update_warehouse_stock(stock_map)

   if len(unfulfilled):
      for order in unfulfilled:
         print(f"order {order.id} not fulfilled")
   else:
      print("all orders fulfilled")

