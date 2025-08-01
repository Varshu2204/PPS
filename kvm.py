import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Initialization
def initialize_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Create doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            is_on_leave BOOLEAN NOT NULL
        )
    ''')

    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            severity INTEGER NOT NULL,
            emergency BOOLEAN NOT NULL,
            doctor_id INTEGER,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    ''')

    # Prepopulate doctor data
    cursor.execute('''
        INSERT OR IGNORE INTO doctors (id, name, is_on_leave) VALUES 
        (1, 'Dr. Smith', 0),
        (2, 'Dr. Jane Doe', 1),
        (3, 'Dr. Emily Carter', 0),
        (4, 'Dr. Robert Brown', 0)
    ''')
    conn.commit()
    conn.close()

# Fetch data functions
def get_doctors():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return doctors

def get_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY emergency DESC, severity DESC")
    patients = cursor.fetchall()
    conn.close()
    return patients

# Add patient function
def add_patient(name, severity, emergency):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, severity, emergency) VALUES (?, ?, ?)",
                   (name, severity, emergency))
    conn.commit()
    conn.close()

# Assign patients to doctors
def assign_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Fetch doctors and patients
    cursor.execute("SELECT * FROM doctors WHERE is_on_leave = 0")
    available_doctors = cursor.fetchall()

    cursor.execute("SELECT * FROM patients WHERE status = 'Pending' ORDER BY emergency DESC, severity DESC")
    pending_patients = cursor.fetchall()

    for patient in pending_patients:
        if not available_doctors:
            break

        doctor = available_doctors.pop(0)  # Assign the first available doctor
        cursor.execute("UPDATE patients SET doctor_id = ?, status = 'Assigned' WHERE id = ?",
                       (doctor[0], patient[0]))

    conn.commit()
    conn.close()

# GUI Application
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Prioritization System - BMS Hospital")

        # Frames
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Doctor Table
        doctor_frame = ttk.Labelframe(self.main_frame, text="Doctors")
        doctor_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.doctor_table = ttk.Treeview(doctor_frame, columns=("ID", "Name", "Available"), show="headings")
        self.doctor_table.heading("ID", text="ID")
        self.doctor_table.heading("Name", text="Name")
        self.doctor_table.heading("Available", text="Available")
        self.doctor_table.grid(row=0, column=0, padx=5, pady=5)

        # Patient Table
        patient_frame = ttk.Labelframe(self.main_frame, text="Patients")
        patient_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.patient_table = ttk.Treeview(patient_frame, columns=("ID", "Name", "Severity", "Emergency", "Status"), show="headings")
        self.patient_table.heading("ID", text="ID")
        self.patient_table.heading("Name", text="Name")
        self.patient_table.heading("Severity", text="Severity")
        self.patient_table.heading("Emergency", text="Emergency")
        self.patient_table.heading("Status", text="Status")
        self.patient_table.grid(row=0, column=0, padx=5, pady=5)

        # Add Patient Section
        add_patient_frame = ttk.Labelframe(self.main_frame, text="Add New Patient")
        add_patient_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        ttk.Label(add_patient_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.patient_name_entry = ttk.Entry(add_patient_frame)
        self.patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_patient_frame, text="Severity:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.severity_entry = ttk.Entry(add_patient_frame)
        self.severity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_patient_frame, text="Emergency:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.emergency_var = tk.BooleanVar()
        ttk.Checkbutton(add_patient_frame, variable=self.emergency_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(add_patient_frame, text="Add Patient", command=self.add_patient).grid(row=3, column=0, columnspan=2, pady=10)

        # Action Buttons
        ttk.Button(self.main_frame, text="Refresh Data", command=self.refresh_data).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Assign Patients", command=self.assign_patients_and_refresh).grid(row=2, column=1, pady=10)

        self.refresh_data()

    def refresh_data(self):
        # Refresh doctor data
        self.doctor_table.delete(*self.doctor_table.get_children())
        for doctor in get_doctors():
            self.doctor_table.insert("", tk.END, values=(doctor[0], doctor[1], "No" if doctor[2] else "Yes"))

        # Refresh patient data
        self.patient_table.delete(*self.patient_table.get_children())
        for patient in get_patients():
            self.patient_table.insert("", tk.END, values=(patient[0], patient[1], patient[2], "Yes" if patient[3] else "No", patient[5]))

    def add_patient(self):
        name = self.patient_name_entry.get()
        try:
            severity = int(self.severity_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Severity must be a number.")
            return
        emergency = self.emergency_var.get()

        if not name:
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return

        add_patient(name, severity, emergency)
        messagebox.showinfo("Success", "Patient added successfully.")
        self.refresh_data()

    def assign_patients_and_refresh(self):
        assign_patients()
        self.refresh_data()

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
