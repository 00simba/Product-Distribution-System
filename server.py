import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
import updatestock_pb2
import updatestock_pb2_grpc
import getstock_pb2
import getstock_pb2_grpc
from concurrent import futures
import logging

class WareHouseServicer(warehouse_pb2_grpc.WarehouseServiceServicer):
    def warehouseInformation(self, request, context):
        warehouseInfo = []
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                warehouseInfo.append(warehouse_pb2.Location.Tuple(id=values[0], x=values[1], y=values[2], capacity=values[3]))

        return warehouse_pb2.Location(warehouseInfo=warehouseInfo)

class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    def orderInformation(self, request, context):
        orderInfo = []
        with open("./files/orders.txt", "r") as f:
            for line in f:
                values = line.split()
                orderInfo.append(order_pb2.OrderInformation.Tuple(id=values[0], x=values[1], y=values[2], quantity=values[3]))

        return order_pb2.OrderInformation(orderInfo=orderInfo)

class UpdateStockServicer(updatestock_pb2_grpc.UpdateWarehouseServiceServicer):
    
    def proto_to_dict(self, hash_map):
        result = {}
        for entry in hash_map.entries:
            result[entry.key] = entry.value
        return result

    def updateStock(self, request, context):
        received_dict = self.proto_to_dict(request)

        new_lines = []

        with open("./files/warehouse.txt", "r") as f:  
            for line in f:
                cur_line = line.split()
                for k, v in received_dict.items():
                    warehouse_id = line.split()[0]
                    warehouse_stock = int(line.split()[-1])
                    if(k == warehouse_id):
                        new_stock = warehouse_stock - int(v)
                        cur_line[-1] = str(new_stock)
                new_lines.append(cur_line)

        with open('./files/warehouse.txt', "w") as f:
            for line in new_lines:
                f.write(" ".join(line) + "\n")
                
        return updatestock_pb2.Response(message="successfully updated warehouse stock")
    
class GetStockServicer(getstock_pb2_grpc.GetWarehouseServiceServicer):

    def getStock(self, request, context):
        stockInfo = []
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                stockInfo.append(getstock_pb2.StockInformation.Tuple(warehouse_id=values[0], warehouse_stock=values[-1]))
        
        return getstock_pb2.StockInformation(stockInfo=stockInfo)
        

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_WarehouseServiceServicer_to_server(WareHouseServicer(), server)
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    updatestock_pb2_grpc.add_UpdateWarehouseServiceServicer_to_server(UpdateStockServicer(), server)
    getstock_pb2_grpc.add_GetWarehouseServiceServicer_to_server(GetStockServicer(), server)
    print("Server Started")
    logging.basicConfig()
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    
    main()