########################################################
##
## FILE:    service_flow.py
## PURPOSE: Create a medical service for the public
## AUTHOR:  JCHARLESCS — special thanks to Niko Bellic.
##          Unlike the pizza system, this code uses OOP, modularizing
##          the project.
##          A patient can take a ticket and wait for their turn to be 
##          served by one of the attendants. Each attendant has their 
##          own counter, which will be useful for generating the 
##          ticket slip that includes the counter number.
##
## VERSION: 1.0
## DATE:    2025-04-11
##
########################################################

from patient import Patient
from ticket_generator import TicketGenerator
from attendant import Attendant
import time
import os

class ServiceFlow:
    def __init__(self):
        self.generator = TicketGenerator()
        self.specialties = [
            {"Cod": "(CLG) - General Practice", "Offices": 3},
            {"Cod": "(GIN) - Gynecology", "Offices": 2},
            {"Cod": "(PED) - Pediatrics", "Offices": 2},
            {"Cod": "(GER) - Geriatrics", "Offices": 2},
            {"Cod": "(ORT) - Orthopedics", "Offices": 2},
        ]
        self.patients = []
        self.tickets = []
        self.queue = []

    def sort_queue(self):
        preferential = [t for t in self.queue if t[3] == "P"]
        normal = [t for t in self.queue if t[3] == "N"]
        self.queue = preferential + normal

    def start(self):
        print("\nWelcome to medical service!\n")
        print("Available specialties:")
        codes = [spec["Cod"][1:4] for spec in self.specialties]
        
        for spec in self.specialties:
            print(spec["Cod"])
        
        code = input("Enter the desired specialty code: ").upper()
        if code not in codes:
            print("Invalid specialty.")
            return

        service_type = input("Type of service (N)ormal | (P)referential: ").capitalize()
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        complaint = input("Describe your complaint: ")

        ticket = self.generator.generate(code, service_type)
        patient = Patient(name, age, service_type, code, complaint, ticket)
        self.patients.append(patient)

        print(f"\nRegistration successful! Your ticket is: {ticket}")
        specialist = [spec["Cod"] for spec in self.specialties if spec["Cod"][1:4] == code]
        print(f"Referred to: ", *specialist)
        print("-" * 40)

        self.tickets.append(ticket)
        self.queue.append(ticket)
        self.sort_queue()

    def call_ticket(self):
        att_1 = Attendant("Victor", "19", "1")
        att_2 = Attendant("Nicolas", "19", "2")

        print(f"\n=== Calling next ticket ===")
        if self.queue:
            next_ticket = self.queue.pop(0)
            counter = att_1.counter if int(next_ticket[-1]) % 2 == 0 else att_2.counter
            print(f"Called ticket: {next_ticket} - Please proceed to counter {counter}")
        else:
            print("No tickets in queue.")

        print("\n=== Current queue (sorted) ===")
        for idx, ticket in enumerate(self.queue, start=1):
            type_desc = "Preferential" if ticket[3] == "P" else "Normal"
            print(f"{idx:02d}. {ticket} - {type_desc}")

    def run_service(self):
        print("\n=== Starting automatic ticket calls ===")
        while self.queue:
            self.call_ticket()
            time.sleep(5)
        print("Queue is empty. No tickets left.")

    def list_patients(self):
        for patient in self.patients:
            print(patient)
