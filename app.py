import tkinter as tk
from tkinter import ttk
import time
import threading

from patient import Patient
from ticket_generator import TicketGenerator
from attendant import Attendant
from service_flow import ServiceFlow

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Service")
        self.flow = ServiceFlow()
        self.generator = TicketGenerator()
        self.auto_calling = False

        self.attendant_1 = Attendant("Manoel", "20", "1")
        self.attendant_2 = Attendant("Victor", "19", "2")

        self.build_interface()

    def build_interface(self):
        # Main Frame (Container)
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()

        # -------------------- Registration --------------------
        registration_frame = tk.LabelFrame(main_frame, text="Patient Registration", padx=10, pady=10)
        registration_frame.grid(row=0, column=0, sticky="nw")

        tk.Label(registration_frame, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(registration_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(registration_frame, text="Age").grid(row=1, column=0)
        self.age_entry = tk.Entry(registration_frame)
        self.age_entry.grid(row=1, column=1)

        tk.Label(registration_frame, text="Complaint").grid(row=2, column=0)
        self.complaint_entry = tk.Entry(registration_frame)
        self.complaint_entry.grid(row=2, column=1)

        tk.Label(registration_frame, text="Type").grid(row=3, column=0)
        self.type_var = tk.StringVar(value="N")
        ttk.Combobox(registration_frame, textvariable=self.type_var, values=["N", "P"]).grid(row=3, column=1)

        tk.Label(registration_frame, text="Specialty").grid(row=4, column=0)
        self.specialty_var = tk.StringVar()
        codes = [code["Cod"][1:4] for code in self.flow.specialties]
        ttk.Combobox(registration_frame, textvariable=self.specialty_var, values=codes).grid(row=4, column=1)

        tk.Button(registration_frame, text="Register Patient", command=self.register_patient).grid(row=5, column=0, columnspan=2, pady=5)

        # -------------------- Controls --------------------
        control_frame = tk.LabelFrame(main_frame, text="Controls", padx=10, pady=10)
        control_frame.grid(row=1, column=0, sticky="w")

        tk.Button(control_frame, text="Call Next Ticket", command=self.call_next).pack(fill="x")
        tk.Button(control_frame, text="Start Auto Service", command=self.start_auto_call).pack(fill="x", pady=5)
        tk.Button(control_frame, text="Stop Service", command=self.stop_call).pack(fill="x")

        # -------------------- Queue --------------------
        queue_frame = tk.LabelFrame(main_frame, text="Waiting Queue", padx=10, pady=10)
        queue_frame.grid(row=0, column=1, rowspan=2, sticky="n")

        self.queue_text = tk.Text(queue_frame, height=12, width=40)
        self.queue_text.pack()

        # -------------------- Counters --------------------
        counter_frame = tk.LabelFrame(main_frame, text="Counters", padx=10, pady=10)
        counter_frame.grid(row=2, column=0, columnspan=2, sticky="we")

        tk.Label(counter_frame, text="Counter 1").grid(row=0, column=0)
        tk.Label(counter_frame, text="Counter 2").grid(row=0, column=1)

        self.counter1_text = tk.Text(counter_frame, height=3, width=25)
        self.counter1_text.grid(row=1, column=0, padx=5)

        self.counter2_text = tk.Text(counter_frame, height=3, width=25)
        self.counter2_text.grid(row=1, column=1, padx=5)

    # ---------- Logic Functions ----------
    def register_patient(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        complaint = self.complaint_entry.get()
        type_ = self.type_var.get()
        code = self.specialty_var.get()

        ticket = self.flow.generator.generate(code, type_)
        patient = Patient(name, age, type_, code, complaint, ticket)
        self.flow.patients.append(patient)
        self.flow.tickets.append(ticket)
        self.flow.queue.append(ticket)
        self.flow.sort_queue()

        self.queue_text.insert(tk.END, f"\nRegistration complete. Ticket: {ticket}\n")
        self.clear_inputs()
        self.update_queue_display()

    def call_next(self):
        if self.flow.queue:
            ticket = self.flow.queue.pop(0)
            self.queue_text.insert(tk.END, f"\n>> Calling: {ticket}\n")
            self.update_queue_display()
        else:
            self.queue_text.insert(tk.END, "Queue is empty.\n")

    def update_call_display(self, counter, ticket):
        if counter == "1":
            self.counter1_text.delete("1.0", tk.END)
            self.counter1_text.insert(tk.END, f"Calling: {ticket}")
        elif counter == "2":
            self.counter2_text.delete("1.0", tk.END)
            self.counter2_text.insert(tk.END, f"Calling: {ticket}")

        self.update_queue_display()

    def update_queue_display(self):
        self.queue_text.delete("1.0", tk.END)
        self.queue_text.insert(tk.END, "Current Queue:\n" + "-" * 40 + "\n")
        for idx, ticket in enumerate(self.flow.queue, start=1):
            type_desc = "Priority" if ticket[3] == "P" else "Normal"
            self.queue_text.insert(tk.END, f"{idx:02d}. {ticket} - {type_desc}\n")

    def start_auto_call(self):
        if not self.auto_calling:
            self.auto_calling = True
            self.start_attendant_thread(self.attendant_1, self.update_call_display)
            self.start_attendant_thread(self.attendant_2, self.update_call_display)

    def stop_call(self):
        self.auto_calling = False

    def start_attendant_thread(self, attendant, callback=None):
        def loop():
            while self.auto_calling:
                if attendant.can_attend and self.flow.queue:
                    ticket = self.flow.queue.pop(0)
                    attendant.start_attendance()

                    if callback:
                        self.root.after(0, callback, attendant.counter, ticket)

                    print(f"Counter {attendant.counter} attending ticket: {ticket}")
                    time.sleep(10)
                    attendant.finish_attendance()
                else:
                    time.sleep(1)

        threading.Thread(target=loop, daemon=True).start()

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.complaint_entry.delete(0, tk.END)
        self.type_var.set("N")
        self.specialty_var.set("")

# ---------- Execution ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
