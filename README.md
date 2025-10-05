# Patient Prioritization System – BMS Hospital

This desktop application helps hospital staff manage patient intake and doctor assignments based on severity and emergency status. Built with Python and Tkinter, it uses a local SQLite database to store and prioritize patient data.

## Features

- Add new patients with severity and emergency flags  
- View doctor availability and patient status  
- Automatically assign patients to available doctors  
- Refresh and update data in real time  
- Local database initialization with sample doctor data  

## Technologies Used

- Python 3  
- Tkinter (GUI)  
- SQLite (local database)  

## How It Works

- Doctors marked as "on leave" are excluded from assignments  
- Patients are sorted by emergency status and severity  
- Each patient is assigned to the next available doctor  
- Status updates from "Pending" to "Assigned" upon allocation  

## Setup Instructions

1. Clone the repository  
2. Run the Python script:
   ```bash
   python hospital_app.py
   ```
3. The database (`hospital.db`) will be created automatically with sample data  
4. Use the GUI to add patients, view tables, and assign doctors 
