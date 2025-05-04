import os
from service_flow import ServiceFlow
system = ServiceFlow()

while True:
    system.start()
    continue_register = input("Do you want to register another patient? (y/n): ").lower()
    
    if continue_register == "y":
        os.system("cls")
        print("\nRegistered patients:")
        system.list_patients()
        continue

    elif continue_register == "n":
        system.run_service()
