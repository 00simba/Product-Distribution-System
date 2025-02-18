from classes.warehouse import Warehouse
from classes.deliverytruck import DeliveryTruck

def main():

    print("COE892 Group Project")

    # Testing classes

    warehouse1 = Warehouse(100, 25)
    deliverytruck1 = Warehouse(50, True)

    print(warehouse1.radius)
    print(deliverytruck1.capacity)

main()